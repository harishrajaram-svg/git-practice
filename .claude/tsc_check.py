import sys, json, subprocess, os

data = json.load(sys.stdin)

# Get the edited file path
fp = data.get("tool_input", {}).get("file_path") or data.get("tool_response", {}).get("filePath", "")
fp = fp.replace("\\", "/")

# Only run tsc for TypeScript files in the queries directory
if "/queries/" not in fp or not fp.endswith((".ts", ".tsx")):
    sys.exit(0)

# Run tsc --noEmit from the queries directory
queries_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "queries")
result = subprocess.run(
    ["npx.cmd", "tsc", "--noEmit"],
    cwd=queries_dir,
    capture_output=True,
    text=True,
    timeout=30
)

if result.returncode != 0:
    errors = result.stdout.strip() or result.stderr.strip()
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"TypeScript compiler found errors after editing {os.path.basename(fp)}:\n\n{errors}\n\nPlease fix these type errors."
        }
    }
    print(json.dumps(output))
