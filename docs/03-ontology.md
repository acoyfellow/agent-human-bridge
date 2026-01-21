# 03 — Minimal Vocabulary (Ontology)

Design goals:
- small set of terms
- no synonyms in artifacts
- operational definitions
- drift-resistant

## Entities (canonical terms)

### WorkUnit
Smallest deliverable change accepted independently. Contains one audit record.

### MiniSpec
Short list of observable Constraints defining success.

### Constraint
Observable claim that can be checked.

Types (closed set):
- functional
- invariant
- negative
- compatibility
- performance
- security

### CheckSuite
Executable set of Checks + run command + environment.

### Check
Single executable evaluation that passes or fails.

### EvidenceRef
Pointer to concrete execution output (logs/test results).

### FailureSignal
Observed output that at least one Check failed.

### DiffSet
Concrete changes applied between base_ref and final_ref.

### FinalGreen
Observed result that all checks pass (with EvidenceRef).

### SpecDelta
Explicit record of any meaningful change in intent/enforcement, with human decision.

## Rules (anti-drift)

- No synonyms in artifacts (use the canonical terms).
- No untyped constraints.
- No green without red (`first_red.occurred=true` required).
- No silent goalpost moves (any weakening routes through `spec_delta`).

## Compression statement
Constraints are observable; checks are executable; evidence is mandatory; diffs are concrete; intent changes are explicit.
