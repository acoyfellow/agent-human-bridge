# Agent–Human Bridge Spec (AHS)

A small, auditable protocol for **agent-mediated software building** that can pass a **human safety review** without relying on “trust in AI”.

This repo contains:
- A **state machine** describing the workflow
- A **minimal audit trail schema** (YAML/JSON) for each work unit
- A **tiny vocabulary/ontology** to prevent semantic drift
- A **golden record** example you can copy
- A **validator** that checks records for mechanical validity
- A **static viewer** (optional) that renders an audit record for humans

## What this is for

Use this when you want agents to iterate quickly, while humans can verify:
1) intent (MiniSpec), 2) first failure (FirstRed), 3) concrete change (DiffSet), 4) observed passing evidence (FinalGreen), 5) explicit goalpost moves (SpecDelta).

## How this works (at a glance)

1. **Define intent**: write a MiniSpec with observable constraints.
2. **Run checks**: capture the first failure as `first_red` evidence.
3. **Make changes**: record concrete edits in `diff_set`.
4. **Re-run checks**: capture passing evidence in `final_green`.
5. **Handle spec changes**: if intent or checks change, record `spec_delta` and a human decision.

The state machine in `docs/02-state-machine.md` ties each step to an audit artifact, so a human can trace intent → failure → change → green without silent goalpost moves.

## Using the tools

- **Validate a record**: run `python3 tools/validate.py path/to/record.yaml` to check schema + invariants.
- **View a record**: open `site/index.html` and drag in a YAML/JSON record for a lightweight audit view.

## Repository layout

- `docs/`
  - `01-bridge-spec.md` — Bridge specification
  - `02-state-machine.md` — State machine + isomorphism to audit fields
  - `03-ontology.md` — Minimal vocabulary/ontology
- `schemas/`
  - `ahs-audit.schema.json` — JSON Schema for audit records
- `examples/`
  - `golden-record.yaml` — A complete sample record
- `tools/`
  - `validate.py` — Validates YAML/JSON records against schema + invariants
- `site/` (optional)
  - `index.html` — Lightweight viewer for audit records (drag & drop)

## Quick start (local)

### 1) Validate the golden record
```bash
python3 tools/validate.py examples/golden-record.yaml
```

### 2) Validate your own record
```bash
python3 tools/validate.py path/to/your-record.yaml
```

## Deployment options

### Option A: Plain GitHub repo
Commit and use as documentation + tooling. No hosting required.

### Option B: Cloudflare Pages (static viewer + docs)
- Deploy `site/` as a Cloudflare Pages project.
- The viewer is static; no backend required.

See `docs/04-deploy-cloudflare-pages.md`.

## License
MIT


## Adversarial suite
See `docs/06-adversarial-tests.md` and `examples/attacks/`.
