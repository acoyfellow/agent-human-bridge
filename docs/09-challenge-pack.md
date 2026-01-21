# 09 — Challenge Pack Spec (Skeptical Walkthrough)

## Goal
Provide a tiny repo a skeptical human can inspect to falsify or accept the Bridge claims by inspection and one command.

## Pack contents (minimum)
1) realistic, readable code slice (small, non-trivial)
2) a harmless-sounding change request
3) “green” tests that lie or omit a key constraint
4) one silent violation that should be caught by audit rules
5) a complete audit record that the validator rejects
6) a one-line command to run the validator

## Required artifacts
- `README.md` with the scenario, intent, and run command
- `workunit.yaml` (or `.json`) with MiniSpec → FinalGreen fields populated
- `examples/` with the failing evidence referenced by `EvidenceRef`
- `expected.md` (one paragraph): why the record must be rejected

## Acceptance criteria
- A skeptical reviewer can identify the violation without trusting the author.
- Running the validator rejects the record deterministically.
- No external services or hidden data are required to reproduce the rejection.

## Notes
- Keep the pack small enough for a 10–15 minute inspection.
- The “lie” should be plausible (not contrived), but easy to verify by reading the code.
