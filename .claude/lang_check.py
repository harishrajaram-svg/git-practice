"""
PostToolUse hook: runs type checkers for typed languages and tests/linters for untyped ones.
Receives hook JSON on stdin, outputs additionalContext JSON if errors are found.
"""
import sys, json, subprocess, os, shutil

data = json.load(sys.stdin)

# Get the edited file path
fp = data.get("tool_input", {}).get("file_path") or data.get("tool_response", {}).get("filePath", "")
fp = fp.replace("\\", "/")
ext = os.path.splitext(fp)[1].lower()
basename = os.path.basename(fp)
filedir = os.path.dirname(fp)

IS_WIN = sys.platform == "win32"


def cmd_exists(name):
    """Check if a command is available on PATH."""
    # On Windows, also check for .cmd/.exe variants
    if IS_WIN:
        for suffix in ["", ".cmd", ".exe"]:
            if shutil.which(name + suffix):
                return True
        return False
    return shutil.which(name) is not None


def find_project_root(start, markers):
    """Walk up from start looking for a directory containing any of the marker files."""
    d = start
    while True:
        for m in markers:
            if os.path.exists(os.path.join(d, m)):
                return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def npx(args):
    """Return npx command adjusted for Windows."""
    return ["npx.cmd" if IS_WIN else "npx"] + args


def run(cmd, cwd=None, timeout=60):
    """Run a command and return (returncode, combined output)."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        output = (result.stdout.strip() + "\n" + result.stderr.strip()).strip()
        return result.returncode, output
    except FileNotFoundError:
        return -1, f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return -1, f"Timed out after {timeout}s"


def report(language, checker, errors):
    """Print hook JSON that feeds errors back to Claude."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"{language} {checker} found errors after editing {basename}:\n\n"
                f"{errors}\n\n"
                f"Please fix these errors."
            )
        }
    }))


# ── Typed languages: type checkers ──────────────────────────────────────────

if ext in (".ts", ".tsx"):
    root = find_project_root(filedir, ["tsconfig.json"])
    if root:
        code, out = run(npx(["tsc", "--noEmit"]), cwd=root)
        if code != 0:
            report("TypeScript", "compiler (tsc --noEmit)", out)

elif ext in (".py", ".pyi"):
    # mypy for type checking
    if cmd_exists("mypy"):
        code, out = run(["mypy", fp, "--no-error-summary"])
        if code != 0:
            report("Python", "type checker (mypy)", out)
    # Fall back to py_compile syntax check
    else:
        code, out = run([sys.executable, "-m", "py_compile", fp])
        if code != 0:
            report("Python", "syntax check (py_compile)", out)

elif ext in (".java",):
    root = find_project_root(filedir, ["pom.xml", "build.gradle", "build.gradle.kts"])
    if root:
        if os.path.exists(os.path.join(root, "pom.xml")):
            code, out = run(["mvn", "compile", "-q"], cwd=root)
        elif os.path.exists(os.path.join(root, "build.gradle")) or os.path.exists(os.path.join(root, "build.gradle.kts")):
            gradle = "gradlew.bat" if IS_WIN else "./gradlew"
            if os.path.exists(os.path.join(root, gradle.replace("./", ""))):
                code, out = run([gradle, "compileJava", "-q"], cwd=root)
            else:
                code, out = run(["gradle", "compileJava", "-q"], cwd=root)
        else:
            code, out = -1, ""
        if code != 0 and out:
            report("Java", "compiler", out)
    elif cmd_exists("javac"):
        code, out = run(["javac", "-Xlint:all", fp])
        if code != 0:
            report("Java", "compiler (javac)", out)

elif ext in (".go",):
    root = find_project_root(filedir, ["go.mod"])
    cwd = root or filedir
    if cmd_exists("go"):
        code, out = run(["go", "vet", "./..."], cwd=cwd)
        if code != 0:
            report("Go", "vet", out)

elif ext in (".rs",):
    root = find_project_root(filedir, ["Cargo.toml"])
    if root and cmd_exists("cargo"):
        code, out = run(["cargo", "check", "--message-format=short"], cwd=root, timeout=120)
        if code != 0:
            report("Rust", "compiler (cargo check)", out)

elif ext in (".cs",):
    root = find_project_root(filedir, ["*.csproj", "*.sln"])
    # dotnet build is more reliable for finding the project
    if not root:
        root = find_project_root(filedir, [f for f in os.listdir(filedir) if f.endswith((".csproj", ".sln"))] if os.path.isdir(filedir) else [])
    if cmd_exists("dotnet"):
        code, out = run(["dotnet", "build", "--no-restore", "-v", "q"], cwd=root or filedir)
        if code != 0:
            report("C#", "compiler (dotnet build)", out)

elif ext in (".kt", ".kts"):
    root = find_project_root(filedir, ["build.gradle", "build.gradle.kts"])
    if root:
        gradle = "gradlew.bat" if IS_WIN else "./gradlew"
        if os.path.exists(os.path.join(root, gradle.replace("./", ""))):
            code, out = run([gradle, "compileKotlin", "-q"], cwd=root)
        elif cmd_exists("gradle"):
            code, out = run(["gradle", "compileKotlin", "-q"], cwd=root)
        else:
            code, out = -1, ""
        if code != 0 and out:
            report("Kotlin", "compiler", out)

elif ext in (".scala",):
    root = find_project_root(filedir, ["build.sbt"])
    if root and cmd_exists("sbt"):
        code, out = run(["sbt", "compile"], cwd=root, timeout=120)
        if code != 0:
            report("Scala", "compiler (sbt compile)", out)

elif ext in (".swift",):
    root = find_project_root(filedir, ["Package.swift"])
    if root and cmd_exists("swift"):
        code, out = run(["swift", "build"], cwd=root, timeout=120)
        if code != 0:
            report("Swift", "compiler (swift build)", out)

elif ext in (".c", ".h"):
    if cmd_exists("gcc"):
        code, out = run(["gcc", "-fsyntax-only", "-Wall", fp])
        if code != 0:
            report("C", "syntax check (gcc)", out)

elif ext in (".cpp", ".cc", ".cxx", ".hpp"):
    if cmd_exists("g++"):
        code, out = run(["g++", "-fsyntax-only", "-Wall", fp])
        if code != 0:
            report("C++", "syntax check (g++)", out)

# ── Untyped languages: linters and tests ────────────────────────────────────

elif ext in (".js", ".jsx", ".mjs", ".cjs"):
    root = find_project_root(filedir, ["package.json"])
    if root:
        # ESLint if available
        eslint_rc = any(
            os.path.exists(os.path.join(root, f))
            for f in [".eslintrc.json", ".eslintrc.js", ".eslintrc.yml", ".eslintrc", "eslint.config.js", "eslint.config.mjs"]
        )
        if eslint_rc:
            code, out = run(npx(["eslint", "--no-error-on-unmatched-pattern", fp]), cwd=root)
            if code != 0:
                report("JavaScript", "linter (eslint)", out)
        # Else syntax check with Node
        else:
            code, out = run(["node", "--check", fp])
            if code != 0:
                report("JavaScript", "syntax check (node --check)", out)

elif ext in (".rb",):
    if cmd_exists("ruby"):
        code, out = run(["ruby", "-c", fp])
        if code != 0:
            report("Ruby", "syntax check (ruby -c)", out)

elif ext in (".php",):
    if cmd_exists("php"):
        code, out = run(["php", "-l", fp])
        if code != 0:
            report("PHP", "syntax check (php -l)", out)

elif ext in (".sh", ".bash"):
    if cmd_exists("shellcheck"):
        code, out = run(["shellcheck", fp])
        if code != 0:
            report("Shell", "linter (shellcheck)", out)
    else:
        code, out = run(["bash", "-n", fp])
        if code != 0:
            report("Shell", "syntax check (bash -n)", out)

elif ext in (".lua",):
    if cmd_exists("luac"):
        code, out = run(["luac", "-p", fp])
        if code != 0:
            report("Lua", "syntax check (luac)", out)

elif ext in (".pl", ".pm"):
    if cmd_exists("perl"):
        code, out = run(["perl", "-c", fp])
        if code != 0:
            report("Perl", "syntax check (perl -c)", out)

elif ext in (".ex", ".exs"):
    root = find_project_root(filedir, ["mix.exs"])
    if root and cmd_exists("mix"):
        code, out = run(["mix", "compile", "--warnings-as-errors"], cwd=root)
        if code != 0:
            report("Elixir", "compiler (mix compile)", out)

elif ext in (".dart",):
    if cmd_exists("dart"):
        code, out = run(["dart", "analyze", fp])
        if code != 0:
            report("Dart", "analyzer", out)
