---
description: Run npm audit to find and fix vulnerable dependencies, then verify with tests
allowed-tools: [Bash]
---

# Dependency Audit

Run a full dependency vulnerability audit, apply fixes, and verify nothing broke.

## Steps

1. Run `npm audit` to identify vulnerable installed packages. Show the user a summary of the findings.
2. If vulnerabilities are found, run `npm audit fix` to apply safe updates automatically.
3. After fixes are applied, run the project's test suite to verify the updates didn't break anything.
4. Summarize what was found, what was fixed, and whether tests still pass.

If `npm audit fix` cannot resolve all issues, inform the user which vulnerabilities remain and suggest running `npm audit fix --force` (with a warning that it may include breaking changes).
