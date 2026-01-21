# 01 — Bridge Specification

## Problem statement (neutral)

Software engineering has historically optimized for correctness under conditions where feedback is slow and failure is expensive.
Agentic tooling makes generation/execution/observation cheaper, creating tension with practices built around pre-execution control.

This spec defines a **compatibility bridge**, not a replacement.

## Preserved invariants (must not change)

1. **Correctness is externally defined** (not inferred from generation).
2. **Responsibility is non-transferable** (the acceptor owns outcomes).
3. **Failure is more informative than success** (under uncertainty).
4. **Observability precedes confidence** (confidence without evidence is speculation).

Any workflow violating these invariants is out of spec.

## Traditional control loop (reference)

Model → Code → Test → Execute → Observe → Revise  
Control is exercised primarily **before execution**.

## Agent-mediated loop (reordered, invariant-preserving)

Constraints → Generate → Execute → Observe failure → Iterate → Human acceptance

No new authority is introduced. Only the **timing of execution and observation** changes.

## Bridge mechanism (key insight)

Control shifts from **preventing incorrect states** to **rapidly eliminating incorrect states**,
while preserving external correctness and human acceptance boundaries.

## Relationship to TDD

TDD already encodes failure-first, external correctness, iterative refinement.
Agent-mediated building is compatible only if it accelerates meaningful failure discovery **without redefining correctness**.

## Applicability constraints

Valid when:
- failures are observable,
- constraints are explicit,
- execution is cheap relative to reasoning,
- a human acceptance boundary exists.

Out of spec when:
- failure is catastrophic/irreversible,
- observability is poor,
- success masks latent harm,
- responsibility is obscured.

## Compression statement

Agent-mediated building preserves deterministic engineering by reordering its control loop:
**execution and failure discovery occur earlier**, while correctness and responsibility remain external and unchanged.
