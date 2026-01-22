# Project Loop

The project loop provides disciplined iteration management for this repository.

## What the Loop Is

A system that:
- Executes one story per git commit
- Enforces tests-first development
- Requires verification before commits
- Uses git commits as the durable memory layer

## Required Files

- `scripts/loop/prd.json` - Product Requirements Document with stories
- `scripts/loop/run.py` - Loop execution script
- `scripts/loop/progress.txt` - Append-only progress log
- `scripts/loop/README.md` - This file

## One Story Per Iteration Rule

Each iteration:
1. Selects highest-priority pending story with completed dependencies
2. Checks test file exists (tests first)
3. Runs verification command
4. Updates status and commits if successful

## How to Run Locally

```bash
python scripts/loop/run.py
```

This will execute one iteration and either succeed (ready to commit) or fail (with logged reason).

## Git Commits as Memory

- Every successful iteration becomes a commit
- Message format: `feat: [ID] - [Title]`
- PRD and progress files track state between runs
