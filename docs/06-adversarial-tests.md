# 06 — Adversarial Tests

Attack records live in `examples/attacks/` and should be rejected by the validator.

Run:
```bash
python3 tools/validate.py examples/attacks/attack-0001-fake-red-empty.yaml
python3 tools/validate.py examples/attacks/attack-0002-green-without-red.yaml
python3 tools/validate.py examples/attacks/attack-0003-spec-changed-no-decision.yaml
python3 tools/validate.py examples/attacks/attack-0004-untyped-constraint.yaml
```

These represent common failure modes:
- counterfeit “red”
- skipping red entirely
- silent goalpost moves
- semantic drift in constraints
