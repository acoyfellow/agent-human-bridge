# 08 — Relevance via Constraint–Check Coupling

## Problem
A WorkUnit can satisfy “no green without red” while the red is unrelated to the stated intent.

This creates false confidence:
- a failure happened,
- something changed,
- everything is green,
- but the failure did not exercise the risk.

## Minimal remedy
Introduce a **Constraint–Check Coupling** classifier.

### Field
Add `coupling` to each `first_red.failing_checks[]` entry:

- `direct`: failing implies a meaningful violation of the constraint.
- `indirect`: supports the constraint, but needs interpretation.
- `incidental`: correlated failure that does not exercise the intent.

### Rule
For each constraint of type:
- `functional`
- `negative`

Require **at least one direct failing check** in FirstRed.

### Why this is human-auditable
Humans can dispute a coupling label directly:
- “This is not direct.”
- “This check does not actually enforce C2.”

Disagreement becomes mechanical, not rhetorical.

## Notes
This does not claim completeness. It only refuses irrelevant evidence.
