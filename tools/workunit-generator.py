#!/usr/bin/env python3
"""
WorkUnit Generator Scaffold

Interactive CLI tool for creating valid WorkUnits with real-time validation feedback.
Guides users through each section and validates compliance.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

def load_schema() -> dict:
    """Load the audit schema for validation."""
    schema_path = Path(__file__).parent.parent / "schemas" / "ahs-audit.schema.json"
    with open(schema_path) as f:
        return json.load(f)

def prompt_with_validation(prompt: str, validator=None, required=True) -> str:
    """Prompt user with optional validation."""
    while True:
        value = input(f"{prompt}: ").strip()
        if not value and required:
            print("This field is required.")
            continue
        if validator and not validator(value):
            print("Invalid input. Please try again.")
            continue
        return value

def create_metadata() -> dict:
    """Collect basic metadata."""
    print("\n=== Basic Metadata ===")
    
    work_id = prompt_with_validation("Work ID (e.g., WU-001-fix-bug)")
    timestamp_utc = datetime.utcnow().isoformat() + "Z"
    repo_ref = prompt_with_validation("Repository reference (e.g., myorg/myrepo@main)")
    
    print("\n=== Actor Information ===")
    human = prompt_with_validation("Human actor (leave empty if none)", required=False)
    agent = prompt_with_validation("Agent actor (leave empty if none)", required=False)
    
    return {
        "audit_version": "1.0",
        "work_id": work_id,
        "timestamp_utc": timestamp_utc,
        "repo_ref": repo_ref,
        "actor": {
            "human": human or None,
            "agent": agent or None
        }
    }

def create_mini_spec() -> dict:
    """Collect mini spec information."""
    print("\n=== Mini Spec ===")
    
    summary = prompt_with_validation("Work summary")
    
    print("\n=== Constraints ===")
    constraints = []
    while True:
        add_constraint = input("Add a constraint? (y/n): ").lower().strip()
        if add_constraint != 'y':
            break
        
        constraint_id = prompt_with_validation("Constraint ID (e.g., C1)")
        statement = prompt_with_validation("Constraint statement")
        
        print("Constraint types: functional, invariant, negative, compatibility, performance, security")
        constraint_type = prompt_with_validation(
            "Constraint type",
            validator=lambda x: x in ["functional", "invariant", "negative", "compatibility", "performance", "security"]
        )
        
        constraints.append({
            "id": constraint_id,
            "statement": statement,
            "type": constraint_type
        })
    
    print("\n=== Out of Scope ===")
    out_of_scope = []
    while True:
        item = input("Out of scope item (leave empty to finish): ").strip()
        if not item:
            break
        out_of_scope.append(item)
    
    return {
        "summary": summary,
        "constraints": constraints,
        "out_of_scope": out_of_scope
    }

def create_check_suite() -> dict:
    """Collect check suite information."""
    print("\n=== Check Suite ===")
    
    location = prompt_with_validation("Test location (e.g., tests/test_feature.py)")
    run_command = prompt_with_validation("Run command (e.g., pytest -v)")
    environment = prompt_with_validation("Environment (e.g., python3.11 + pytest)")
    
    return {
        "location": location,
        "run_command": run_command,
        "environment": environment
    }

def create_first_red(constraints: list) -> dict:
    """Collect first red information."""
    print("\n=== First Red ===")
    
    occurred_input = prompt_with_validation("Did red occur? (true/false)", validator=lambda x: x.lower() in ["true", "false"])
    occurred = occurred_input.lower() == "true"
    
    failing_checks = []
    if occurred:
        print("\n=== Failing Checks ===")
        constraint_ids = [c["id"] for c in constraints]
        
        while True:
            add_check = input("Add a failing check? (y/n): ").lower().strip()
            if add_check != 'y':
                break
            
            check_id = prompt_with_validation("Check ID (e.g., test_feature_fails)")
            
            print(f"Available constraint IDs: {', '.join(constraint_ids)}")
            check_constraint_ids = []
            while True:
                cid = input("Constraint ID this check exercises (leave empty to finish): ").strip()
                if not cid:
                    break
                if cid not in constraint_ids:
                    print(f"Warning: {cid} not in defined constraints")
                check_constraint_ids.append(cid)
            
            coupling_options = ["direct", "indirect", "incidental"]
            print(f"Coupling options: {', '.join(coupling_options)}")
            coupling = prompt_with_validation("Coupling type", validator=lambda x: x in coupling_options)
            
            evidence_ref = prompt_with_validation("Evidence reference (e.g., logs/first_red.txt)")
            
            failing_checks.append({
                "check_id": check_id,
                "constraint_ids": check_constraint_ids,
                "evidence_ref": evidence_ref,
                "coupling": coupling
            })
    
    return {
        "occurred": occurred,
        "failing_checks": failing_checks
    }

def create_diff_set(constraints: list) -> dict:
    """Collect diff set information."""
    print("\n=== Diff Set ===")
    
    base_ref = prompt_with_validation("Base reference (e.g., abc123)")
    final_ref = prompt_with_validation("Final reference (e.g., def456)")
    
    print("\n=== Files Changed ===")
    files_changed = []
    while True:
        add_file = input("Add a changed file? (y/n): ").lower().strip()
        if add_file != 'y':
            break
        
        file_path = prompt_with_validation("File path")
        change_types = ["modified", "added", "deleted", "renamed"]
        print(f"Change types: {', '.join(change_types)}")
        change_type = prompt_with_validation("Change type", validator=lambda x: x in change_types)
        
        files_changed.append({
            "path": file_path,
            "change_type": change_type
        })
    
    print("\n=== Rationale ===")
    rationale = []
    constraint_ids = [c["id"] for c in constraints]
    
    for constraint in constraints:
        print(f"Note for constraint {constraint['id']}: {constraint['statement'][:50]}...")
        note = input(f"Rationale note (leave empty to skip): ").strip()
        if note:
            rationale.append({
                "constraint_id": constraint["id"],
                "note": note
            })
    
    return {
        "base_ref": base_ref,
        "final_ref": final_ref,
        "files_changed": files_changed,
        "rationale": rationale
    }

def create_final_green() -> dict:
    """Collect final green information."""
    print("\n=== Final Green ===")
    
    all_checks_passed_input = prompt_with_validation("All checks passed? (true/false)", validator=lambda x: x.lower() in ["true", "false"])
    all_checks_passed = all_checks_passed_input.lower() == "true"
    
    if all_checks_passed:
        run_id = prompt_with_validation("Run ID (e.g., run-2026-01-22T10:00:00Z)")
        evidence_ref = prompt_with_validation("Evidence reference (e.g., logs/final_green.txt)")
        
        print("\n=== Summary Metrics ===")
        duration_seconds = float(prompt_with_validation("Duration in seconds", validator=lambda x: x.replace(".", "").isdigit()))
        checks_executed = int(prompt_with_validation("Checks executed", validator=lambda x: x.isdigit()))
        
        summary_metrics = {
            "duration_seconds": duration_seconds,
            "checks_executed": checks_executed
        }
    else:
        run_id = ""
        evidence_ref = ""
        summary_metrics = {}
    
    return {
        "all_checks_passed": all_checks_passed,
        "run_id": run_id,
        "evidence_ref": evidence_ref,
        "summary_metrics": summary_metrics
    }

def create_spec_delta() -> dict:
    """Collect spec delta information."""
    print("\n=== Spec Delta ===")
    
    changed_input = prompt_with_validation("Spec changed? (true/false)", validator=lambda x: x.lower() in ["true", "false"])
    changed = changed_input.lower() == "true"
    
    changes = []
    if changed:
        print("\n=== Changes ===")
        change_kinds = ["constraint", "check"]
        while True:
            add_change = input("Add a change? (y/n): ").lower().strip()
            if add_change != 'y':
                break
            
            print(f"Change kinds: {', '.join(change_kinds)}")
            kind = prompt_with_validation("Change kind", validator=lambda x: x in change_kinds)
            change_id = prompt_with_validation("Change ID")
            before = prompt_with_validation("Before value")
            after = prompt_with_validation("After value")
            reason = prompt_with_validation("Reason for change")
            
            changes.append({
                "kind": kind,
                "id": change_id,
                "before": before,
                "after": after,
                "reason": reason
            })
    
    if changed:
        human_decision = prompt_with_validation("Human decision (accepted/rejected)", validator=lambda x: x in ["accepted", "rejected"])
    else:
        human_decision = "n/a"
    
    return {
        "changed": changed,
        "changes": changes,
        "human_decision": human_decision
    }

def validate_workunit(workunit: dict) -> bool:
    """Basic validation of the workunit."""
    # Check required fields
    required_fields = ["audit_version", "work_id", "timestamp_utc", "repo_ref", "actor", 
                      "mini_spec", "check_suite", "first_red", "diff_set", "final_green", "spec_delta"]
    
    for field in required_fields:
        if field not in workunit:
            print(f"ERROR: Missing required field '{field}'")
            return False
    
    # Check constraints exist
    constraints = workunit.get("mini_spec", {}).get("constraints", [])
    if not constraints:
        print("ERROR: At least one constraint required")
        return False
    
    # Check first_red logic
    first_red = workunit.get("first_red", {})
    if not first_red.get("occurred", False):
        print("ERROR: First red must occur (no green without red)")
        return False
    
    failing_checks = first_red.get("failing_checks", [])
    if not failing_checks:
        print("ERROR: At least one failing check required when red occurred")
        return False
    
    # Check final_green
    final_green = workunit.get("final_green", {})
    if not final_green.get("all_checks_passed", False):
        print("ERROR: All checks must pass")
        return False
    
    print("WorkUnit validation passed!")
    return True

def save_workunit(workunit: dict, filename: str):
    """Save workunit to YAML file."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required for YAML output. Install with: pip install pyyaml")
        return False
    
    try:
        with open(filename, 'w') as f:
            yaml.dump(workunit, f, default_flow_style=False, sort_keys=False)
        print(f"WorkUnit saved to {filename}")
        return True
    except Exception as e:
        print(f"ERROR saving workunit: {e}")
        return False

def main():
    print("=== WorkUnit Generator Scaffold ===")
    print("This tool will guide you through creating a valid WorkUnit.")
    print("Answer the prompts to build your workunit interactively.")
    print()
    
    workunit = {}
    
    try:
        workunit.update(create_metadata())
        workunit["mini_spec"] = create_mini_spec()
        workunit["check_suite"] = create_check_suite()
        workunit["first_red"] = create_first_red(workunit["mini_spec"]["constraints"])
        workunit["diff_set"] = create_diff_set(workunit["mini_spec"]["constraints"])
        workunit["final_green"] = create_final_green()
        workunit["spec_delta"] = create_spec_delta()
        
        print("\n=== Validation ===")
        if validate_workunit(workunit):
            filename = f"{workunit['work_id']}.yaml"
            if save_workunit(workunit, filename):
                print(f"\nSuccess! Your WorkUnit has been created as {filename}")
                print("You can now validate it with: python tools/validate.py", filename)
            else:
                print("\nFailed to save WorkUnit.")
                return 1
        else:
            print("\nWorkUnit validation failed. Please review and try again.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nGeneration cancelled.")
        return 1
    except Exception as e:
        print(f"\nERROR: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("WorkUnit Generator Scaffold")
        print()
        print("Interactive CLI tool for creating valid WorkUnits.")
        print("Guides through each section with validation feedback.")
        print()
        print("Usage: python tools/workunit-generator.py")
        sys.exit(0)
    
    sys.exit(main())
