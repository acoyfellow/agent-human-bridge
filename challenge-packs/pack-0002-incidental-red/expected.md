# Expected Outcome: SHOULD BE REJECTED

## Why the Current Validator Accepts This

The workunit.yaml passes all current validator rules:
- ✓ first_red.occurred is true
- ✓ At least one failing check exists
- ✓ Failing check is mapped to performance constraints (C3, C4)
- ✓ final_green.all_checks_passed is true
- ✓ spec_delta.changed is false
- ✓ All constraints are properly typed
- ✓ All required fields are present

**Result: VALID** ✓

## Why a Human Reviewer Should Reject This

### The Critical Flaw: Incidental Red

The audit record shows:
- **Claimed risk:** Performance regression in hot path (constraint C1)
- **Failing test:** `test_config_validation_performance`
- **What the test actually measures:** Cold path startup performance (`validate_config`)

### The Deception

1. **Constraint C1** states: "process_batch() maintains throughput of 10,000 items/sec minimum"
   - This is the real performance risk
   - `process_batch()` is the hot path, called thousands of times per second

2. **The failing test** checks: `test_config_validation_performance`
   - This tests `validate_config()`, NOT `process_batch()`
   - `validate_config()` is called ONCE at startup (cold path)
   - The test is mapped to constraints C3 and C4 (secondary performance constraints)

3. **The vulnerability:**
   - The test that failed and turned green does NOT exercise the stated risk in C1
   - No test actually measures hot path performance of `process_batch()`
   - The red is real, the fix is real, but it's **incidental** to the actual risk

### What Could Be Hidden

An agent could:
1. Introduce a subtle performance regression in `process_batch()` (the hot path)
2. Also introduce a separate performance issue in `validate_config()` (the cold path)
3. Fix only the cold path issue to get green
4. Claim the work is complete with "performance validated"

The protocol accepts this because:
- There was a red (in config validation)
- There was a green (in config validation)
- The constraint types are correct (performance)

But a human should reject it because:
- **The red didn't test what matters** (hot path throughput)
- The evidence is structurally correct but **semantically insufficient**

## The Missing Rule

To catch this, the protocol needs:
- **Coupling field:** Label each failing check as `direct`, `indirect`, or `incidental`
- **Relevance rule:** For critical constraints (like C1), require at least one `direct` red

Without this, the protocol accepts **incidental evidence** as if it were **direct evidence**.

## Human Verdict

**REJECT:** The red does not prove safety of the actual performance risk.

The test suite should include:
- A direct hot path throughput test for `process_batch()`
- This test should have failed and then passed
- Only then would the evidence be sufficient
