# AGENTS.md — Grok Build contract

Read this file before writing any code in a consumer repo that this harness
drives (GeoByteLab or otherwise).

## Role

You are an implementation agent. You may propose configs, write tests, write
code, run smoke jobs, and **submit metrics**. You may not declare a scientific
gate passed.

## Mandatory loop

1. Read `AGENTS.md`, `SPEC.md`, the task record, and dependency artifacts.
2. Restate the local contract in `tasks/completed/<id>/CONTRACT.md`.
3. Add or identify a failing test (`RED_TEST`).
4. Implement the smallest change that makes that test pass.
5. Run targeted tests, then `just test-fast`.
6. Inspect the diff for scope creep and causal leakage.
7. If model/data path changed, run `just smoke`.
8. Save evidence under `tasks/completed/<id>/`.
9. Update task state via `gbh task transition`. Never write `passed: true`
   into a gate file by hand.

## Prohibited defaults

Do not encode any of these as assumed facts:

- A fixed Prime-Phase / Prime Crystal framework is a model of language.
- Sheaf compatibility guarantees truth or blocks hallucination.
- A data-independent Koopman operator exists for language dynamics.
- Unit-norm makes every coordinate informative.
- A 64–128D hyperbolic state replaces a 1k–4k Euclidean residual stream.
- Fewer embedding parameters imply less end-to-end compute.
- Topological attractors are the causal basis of reasoning.
- Any geometric module will beat a much larger model without matched evidence.

## Merge blockers

A change cannot merge when:

- a sequence-path change has no causal leakage test;
- a non-smoke run uses an unlocked source revision;
- a new metric is computed differently across baselines;
- hidden defaults are not in the resolved config;
- checkpoint cannot reload on CPU;
- speculative modules altered the baseline path;
- a performance claim uses only theoretical sequence-length reduction;
- license/provenance fields were dropped.

## Geometry and sheaf

Geometry modules are isolated, gated, coefficient-zero by default.
Sheaf energy is allowed only on a **trusted, weight-independent graph**
(AST, section tree, frozen entropy cuts, byte k-neighborhood).
Identity-map (`ρ = I`) and shuffled-edge controls are mandatory.
A path graph has vacuous `δ²`; do not audit `δ²` unless 2-cells are declared.

## Hardware

- `train_5070`: primary bf16 training.
- `aux_1660ti`: entropy model, eval, smoke. Never DDP-sync with the 5070.
- Hard allocated-VRAM ceiling on ordinary 5070 runs: 10.8 GB.

## Gate ownership

```text
agent  -> metrics.json
gbh    -> gate_result.json   (pure function, separate process)
human  -> optional override with written ADR
```
