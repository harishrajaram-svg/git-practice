# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python learning project for practicing Git workflows. Created by Harish Rajaram.

## Running

```bash
python app.py            # prints greeting messages
python calculator.py     # launches interactive calculator menu
python test.py           # verifies Python runs from Git Bash
python api_test.py       # single Claude API call (requires ANTHROPIC_API_KEY env var)
python chat_test.py      # multi-turn Claude API conversation (requires ANTHROPIC_API_KEY env var)
```

## Architecture

- **app.py** — standalone greeting script
- **calculator.py** — arithmetic functions (`add`, `subtract`, `multiply`, `divide`) with an interactive menu via `main()`. Functions are importable: `from calculator import add`
- **test.py** — quick sanity check for the Python/Git Bash environment
- **api_test.py / chat_test.py** — Claude API experiments using the `anthropic` Python SDK. Require `ANTHROPIC_API_KEY` set in the environment.

No build step, linter, or test framework configured. The API scripts require `pip install anthropic`; everything else uses only the standard library.
