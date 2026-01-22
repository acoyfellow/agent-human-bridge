#!/usr/bin/env python3
"""
AHS validator

Validates:
1) JSON Schema (schemas/ahs-audit.schema.json)
2) Mechanical invariants (hard errors)
3) Optional strict checks (warnings) for human-audit friendliness

Usage:
  python3 tools/validate.py examples/golden-record.yaml
  python3 tools/validate.py --strict path/to/record.yaml
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

def load_record(p: Path) -> dict:
    txt = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            raise SystemExit("PyYAML not installed. Install with: pip install pyyaml")
        return yaml.safe_load(txt)
    return json.loads(txt)

def load_schema(schema_path: Path) -> dict:
    return json.loads(schema_path.read_text(encoding="utf-8"))

def schema_validate(schema: dict, record: dict) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        raise SystemExit("jsonschema not installed. Install with: pip install jsonschema")
    v = jsonschema.Draft202012Validator(schema)
    errs = []
    for e in sorted(v.iter_errors(record), key=lambda e: e.path):
        loc = ".".join([str(x) for x in e.path]) or "<root>"
        errs.append(f"{loc}: {e.message}")
    return errs

def invariants(record: dict, record_path: Path | None = None) -> list[str]:
    errs = []
    constraints = record.get("mini_spec", {}).get("constraints", [])
    if not constraints:
        errs.append("mini_spec.constraints must have at least 1 item")

    if record.get("first_red", {}).get("occurred") is not True:
        errs.append("first_red.occurred must be true (no red without green)")

    failing = record.get("first_red", {}).get("failing_checks", [])
    if record.get("first_red", {}).get("occurred") is True and len(failing) < 1:
        errs.append("first_red.failing_checks must have at least 1 item when occurred is true")

    if record.get("final_green", {}).get("all_checks_passed") is not True:
        errs.append("final_green.all_checks_passed must be true")

    spec_delta = record.get("spec_delta", {})
    if spec_delta.get("changed") is True:
        if spec_delta.get("human_decision") not in ("accepted","rejected"):
            errs.append("spec_delta.human_decision must be accepted/rejected when spec_delta.changed is true")
        if not spec_delta.get("changes"):
            errs.append("spec_delta.changes must be non-empty when spec_delta.changed is true")

    # Direct red rule: functional, negative, or performance constraints must have at least one direct red
    critical_types = {"functional", "negative", "performance"}
    critical_constraints = [c for c in constraints if c.get("type") in critical_types]
    
    # Build set of constraint IDs that have direct reds
    direct_red_constraint_ids = set()
    for fc in failing:
        if fc.get("coupling") == "direct":
            direct_red_constraint_ids.update(fc.get("constraint_ids", []))
    
    # Check which critical constraints lack direct reds
    missing_direct_red = [c.get("id") for c in critical_constraints 
                          if c.get("id") not in direct_red_constraint_ids]
    
    if missing_direct_red:
        errs.append(f"Constraints {missing_direct_red} lack a direct red (required for functional, negative, or performance types)")

    # Evidence refs must exist on disk if they look like local paths
    def check_evidence(ref: str, label: str):
        if not ref or "://" in ref:
            return
        if record_path is None:
            return
        p = (record_path.parent / ref).resolve()
        if not p.exists():
            errs.append(f"{label}: evidence_ref '{ref}' does not exist on disk")
    for fc in record.get("first_red", {}).get("failing_checks", []):
        check_evidence(fc.get("evidence_ref",""), f"first_red.{fc.get('check_id','?')}")
    check_evidence(record.get("final_green", {}).get("evidence_ref",""), "final_green")

    return errs

def strict_checks(record: dict, record_path: Path) -> list[str]:
    warns = []
    # Encourage mapping failing checks to constraints
    for fc in record.get("first_red", {}).get("failing_checks", []):
        if not fc.get("constraint_ids"):
            warns.append(f"first_red failing_check '{fc.get('check_id','?')}' has empty constraint_ids (harder to audit)")
    # Evidence refs should exist as files relative to record path, if they look like local paths
    def check_evidence(ref: str, label: str):
        if not ref or "://" in ref:
            return
        p = (record_path.parent / ref).resolve()
        if not p.exists():
            warns.append(f"{label}: evidence_ref '{ref}' does not exist on disk (ok if stored elsewhere)")
    for fc in record.get("first_red", {}).get("failing_checks", []):
        check_evidence(fc.get("evidence_ref",""), f"first_red.{fc.get('check_id','?')}")
    check_evidence(record.get("final_green", {}).get("evidence_ref",""), "final_green")
    return warns

def main() -> int:
    strict = False
    args = [a for a in sys.argv[1:] if a.strip()]
    if not args or len(args) > 2:
        print("Usage: python3 tools/validate.py [--strict] path/to/record.(yaml|json)")
        return 2
    if args[0] == "--strict":
        strict = True
        if len(args) != 2:
            print("Usage: python3 tools/validate.py --strict path/to/record.(yaml|json)")
            return 2
        record_path = Path(args[1]).resolve()
    else:
        record_path = Path(args[0]).resolve()

    root = Path(__file__).resolve().parents[1]
    schema_path = root / "schemas" / "ahs-audit.schema.json"

    record = load_record(record_path)
    schema = load_schema(schema_path)

    errors = []
    errors += schema_validate(schema, record)
    errors += invariants(record, record_path)

    warnings = []
    if strict and not errors:
        warnings = strict_checks(record, record_path)

    if errors:
        print("INVALID\n")
        for e in errors:
            print(f"- {e}")
        return 1

    print("VALID")
    if warnings:
        print("\nWARNINGS")
        for w in warnings:
            print(f"- {w}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
