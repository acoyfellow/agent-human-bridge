# 05 — Minimal Form (Shrink Without Losing Safety)

This defines the smallest record that still preserves the invariants:

- correctness is externally defined
- responsibility is non-transferable
- no green without prior red
- no silent goalpost moves

## Minimal record (AHS-Min)

Required fields:

1) `mini_spec` (constraints, out_of_scope)
2) `check_suite` (run_command, environment, location)
3) `first_red` (occurred=true, failing_checks>=1, evidence_ref)
4) `diff_set` (base_ref, final_ref, files_changed)
5) `final_green` (all_checks_passed=true, evidence_ref, run_id)

Optional but strict:
- `spec_delta` (required if any meaningful spec/check change occurred)

## Hard rules (minimal)

- **R1**: `mini_spec.constraints` non-empty; each constraint has a closed-set type.
- **R2**: `first_red.occurred` must be `true` and include ≥1 failing check.
- **R3**: `final_green.all_checks_passed` must be `true`.
- **R4**: if `spec_delta.changed==true`, `human_decision` is `accepted` or `rejected`.
- **R5**: no deletion/relaxation of failing checks without an explicit `spec_delta` entry.

This is the smallest bridge that still holds human auditability.
