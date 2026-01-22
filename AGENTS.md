# North Star
Leverage without abdication.

Stop condition: loop ends when all stories in PRD are completed and verification is green.

Absolute rules:
- PRD only
- One story per iteration
- Tests first
- Verify before commit
- Git commits are memory

Local development commands for this repo:
- python tools/validate.py …

Known footguns:
- JSON validity
- Hidden / bidi unicode text in files
