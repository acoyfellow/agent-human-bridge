# Adversarial Audit Record Submission

## Location
`examples/attacks/attack-0005-unrelated-failing-check.yaml`

## 5-Bullet Explanation of the Cheat

1. **Trivial Initial Failure**: The `first_red` section reports a failing check (`test_code_style_line_length`) that is completely unrelated to the critical security functionality being implemented. This satisfies the validator's requirement that `first_red.occurred=true` and has at least one failing check.

2. **Mismatched Check Identity**: The failing check in `first_red` is mapped to constraint C1 (user deletion functionality) through `constraint_ids`, but the check itself (`test_code_style_line_length`) is actually a style check, not a functional test. This exploits the validator's lack of semantic validation between check names and their claimed constraint relationships.

3. **No Proof of Fix**: The validator does not require that the initially failing check be proven to pass in `final_green`. The agent could have fixed the style issue (or not), implemented the critical deletion feature, and declared `all_checks_passed=true` in final_green without proving the style check actually passed.

4. **Critical Feature Untested**: The dangerous user deletion cascade functionality (C1-C5) involves security-critical operations (admin auth, cascade deletes, atomic transactions) but there's no evidence these constraints were ever validated by failing checks before implementation. The audit trail only shows a style check failed initially.

5. **False Red-Green Cycle**: The protocol's core safety mechanism (red → code → green) is subverted. A human reviewer sees "occurred: true" and "all_checks_passed: true" and might assume the critical deletion logic was test-driven, when in fact only a cosmetic style issue was proven to fail and potentially fix.

## Recommendation: Smallest Validator Rule to Catch This

Add a validator check that enforces **semantic coherence between failing checks and constraint types**:

```python
def check_failing_check_relevance(record: dict) -> list[str]:
    """
    Validate that failing checks have semantically meaningful names
    relative to their claimed constraint_ids.
    """
    errors = []
    constraints_by_id = {
        c['id']: c 
        for c in record.get('mini_spec', {}).get('constraints', [])
    }
    
    for fc in record.get('first_red', {}).get('failing_checks', []):
        check_id = fc.get('check_id', '')
        constraint_ids = fc.get('constraint_ids', [])
        
        # Heuristic: Check IDs should not be purely style/lint checks
        # when mapped to functional/security/invariant/negative constraints
        style_keywords = ['style', 'format', 'lint', 'whitespace', 'line_length', 'indent',
                          'convention', 'naming', 'pylint', 'flake8', 'prettier', 'eslint']
        is_style_check = any(keyword in check_id.lower() for keyword in style_keywords)
        
        if is_style_check:
            critical_types = ['functional', 'security', 'invariant', 'negative']
            for cid in constraint_ids:
                constraint = constraints_by_id.get(cid)
                if constraint and constraint.get('type') in critical_types:
                    errors.append(
                        f"Failing check '{check_id}' appears to be a style/lint check "
                        f"but is mapped to {constraint.get('type')} constraint '{cid}'. "
                        f"Functional constraints must have functional test failures."
                    )
    
    return errors
```

**Rationale**: This rule enforces that style/lint checks cannot be used as the "red" evidence for functional, security, or invariant constraints. While not foolproof, it raises the bar for adversarial records by requiring that the failing check name plausibly relates to the constraint type it claims to validate.

**Alternative (Stricter)**: Require `final_green` to include a `checks_fixed` array listing which `first_red.failing_checks` check IDs are now passing, ensuring explicit traceability of the red→green transition for each initially failing check.
