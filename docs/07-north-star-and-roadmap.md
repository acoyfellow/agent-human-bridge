# 07 — North Star & Runnable Checkpoints

## North Star (one line)

**Leverage without abdication.**

Operational form:

**Make responsibility visible, relevant, and unavoidable at the moment leverage is applied.**

## What this package already provides (runnable core)

- A **state machine** for agent-mediated building with a human acceptance boundary.
- A **minimal audit trail** schema (YAML/JSON) for each WorkUnit.
- A **minimal ontology** (closed vocabulary) to prevent semantic drift.
- A **validator** that deterministically accepts/rejects records.
- An **adversarial suite** of attack records that should fail.

## Runnable checkpoints

### Checkpoint A — Structural honesty (DONE)
A WorkUnit is rejected unless:
- constraints exist and are typed,
- a real first red exists (no green without red),
- final green exists,
- spec changes are explicit and decided by a human.

### Checkpoint B — Relevance honesty (NEXT)
Add a coupling field to make sure the *right* failure happened.

#### New field
In `first_red.failing_checks[]`:
- `coupling: direct | indirect | incidental`

#### New rule
For each **functional** and **negative** constraint, the WorkUnit must contain at least one **direct** failing check in FirstRed.

Purpose: reject “incidental reds” that do not exercise intent.

### Checkpoint C — Human chewable evidence (NEXT)
Ship a **Challenge Pack**: a tiny repo that a skeptical human can inspect and try to break.

Contents:
1) realistic code slice
2) harmless-sounding change request
3) green tests that lie
4) one silent violation
5) audit record that rejects the claim
6) one command to run the validator

This is the *experience* step: humans can falsify/accept the idea without trusting the author.

## Stop condition
Stop extending the protocol when it can:
- reject structurally dishonest work,
- reject irrelevant evidence,
- and produce a human-auditable trail by default.

Everything after that is deployment and ergonomics (optional).
