---
description: Write tests for a specified file or component
argument-hint: <file-path>
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit]
---

# Write Tests

Write comprehensive tests for: $ARGUMENTS

## Testing Conventions

- Use Vitest with React Testing Library
- Place test files in a `__tests__` directory in the same folder as the source file
- Name test files as `[filename].test.ts(x)`
- Use `@/` prefix for imports

## Steps

1. Read the target file to understand its exports, functions, and behavior.
2. Look at existing test files nearby to match mocking patterns and style.
3. Write tests covering:
   - Happy paths
   - Edge cases
   - Error states
4. Run the new tests to confirm they pass.
