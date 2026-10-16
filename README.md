# grok-build-harness

Grok-executable agentic **code-writing and toolchain** harness.

This is not a language model. It is the residual verification substrate that
lets an agent implement GeoByteLab (or any sibling lab) without stamping its
own scientific gates.

**Status:** implementation scaffold, ready to clone before the first GeoByteLab
commit.

**Target workstation:** i9-9900K / 32 GB DDR4 / RTX 5070 12 GB + GTX 1660 Ti 6 GB.

## What this is

- Task state machine: `BACKLOG → CLAIMED → RED_TEST → IMPLEMENTED → SELF_REVIEWED → INTEGRATION_TESTED → PROFILED_IF_REQUIRED → DONE`
- Scientific gates as **pure functions**. The agent submits metrics; a separate process computes pass/fail; the result is append-only.
- Hardware doctor, GPU class locks (`train_5070` | `aux_1660ti` | `cpu`), source-lock schema.
- Frozen GeoByteLab v2 kill numbers and rejected premises.

## What this is not

- Not the Prime Crystal Engine.
- Not a sheaf-as-truth claim.
- Not a 7–10B vs 60–1000× scaling story.
- Not GeoByteLab itself (`modeling_geobyte.py` lives in a sibling repo).

## Quick start

```bash
uv sync
just doctor
just test-fast
just gate-demo
```

Grok / coding-agent entrypoint: read `AGENTS.md` then `BOOTSTRAP_PROMPT.md`.

## Sibling priors (read, do not merge as default path)

| Repo | Role |
|---|---|
| `maxop-mcp-harness` | Markov/MCP loop, ledger posture |
| `spec-p0-lab` | QK-norm / clamp / σReparam matrix, failed hyps kept |
| `premature-sheafification` | default prior that sheaf-on-inferred-graphs did not earn its keep |
| `comma-residue-lab` | RESTRICT → … → CERTIFY methodology |

## License

This project is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE). Commercial use requires a separate license from the copyright holder, B. Jones (b.jones@jtech.ai). See [NOTICE](NOTICE). Versions published before 2026-10-16 were released under the MIT License, and those versions keep it.
