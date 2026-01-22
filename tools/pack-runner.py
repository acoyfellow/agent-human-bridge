#!/usr/bin/env python3
"""
Challenge Pack Runner

Discovers all challenge packs, runs validator on each, compares to expected outcomes,
and generates a pass/fail report.
"""

import json
import subprocess
import sys
from pathlib import Path

def find_packs(packs_dir: Path):
    """Find all pack directories (pack-XXXX format)."""
    return [d for d in packs_dir.iterdir() if d.is_dir() and d.name.startswith("pack-")]

def get_expected_outcome(pack_dir: Path) -> str:
    """Read expected.md to determine if pack should be VALID or INVALID."""
    expected_file = pack_dir / "expected.md"
    if not expected_file.exists():
        return "UNKNOWN"
    
    content = expected_file.read_text().upper()
    if "INVALID" in content:
        return "INVALID"
    elif "VALID" in content:
        return "VALID"
    return "UNKNOWN"

def run_validator(workunit_path: Path) -> str:
    """Run the validator and return VALID, INVALID, or ERROR."""
    try:
        result = subprocess.run(
            [sys.executable, "tools/validate.py", str(workunit_path)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        if result.returncode == 0:
            return "VALID"
        elif result.returncode == 1:
            return "INVALID"
        else:
            return f"ERROR: {result.stderr.strip()}"
    except Exception as e:
        return f"ERROR: {str(e)}"

def generate_report(results: list) -> str:
    """Generate a formatted report."""
    report = ["# Challenge Pack Runner Report", ""]
    
    passed = 0
    total = len(results)
    
    for pack_name, expected, actual, status in results:
        if status == "PASS":
            passed += 1
        report.append(f"## {pack_name}")
        report.append(f"- Expected: {expected}")
        report.append(f"- Actual: {actual}")
        report.append(f"- Status: {status}")
        report.append("")
    
    report.append("## Summary")
    report.append(f"- Passed: {passed}/{total}")
    report.append(f"- Failed: {total - passed}/{total}")
    
    if passed == total:
        report.append("- Overall: SUCCESS")
    else:
        report.append("- Overall: FAILURE")
    
    return "\n".join(report)

def main():
    repo_root = Path(__file__).parent.parent
    packs_dir = repo_root / "challenge-packs"
    
    if not packs_dir.exists():
        print("ERROR: challenge-packs directory not found")
        return 1
    
    packs = find_packs(packs_dir)
    if not packs:
        print("ERROR: No challenge packs found")
        return 1
    
    results = []
    for pack_dir in packs:
        pack_name = pack_dir.name
        workunit_path = pack_dir / "workunit.yaml"
        expected = get_expected_outcome(pack_dir)
        
        if not workunit_path.exists():
            actual = "ERROR: workunit.yaml not found"
            status = "FAIL"
        else:
            actual = run_validator(workunit_path)
            if expected == "UNKNOWN":
                status = "UNKNOWN"
            elif actual == expected:
                status = "PASS"
            else:
                status = "FAIL"
        
        results.append((pack_name, expected, actual, status))
    
    report = generate_report(results)
    print(report)
    
    # Exit with 0 if all passed, 1 if any failed
    all_passed = all(r[3] == "PASS" for r in results)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
