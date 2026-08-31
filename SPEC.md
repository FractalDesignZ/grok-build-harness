# SPEC.md — harness contract

## 0. Decision

Build a modular agent/toolchain harness that can drive GeoByteLab without
becoming GeoByteLab. The production candidate of any driven LM lab remains:

```text
learned byte embedding
+ causal local encoder
+ empirically winning patch policy
+ Euclidean pre-RMSNorm (or independently gated normalized backbone)
+ causal local decoder
```

Every other mechanism must earn inclusion through a named gate.

## 1. Task state machine

```text
BACKLOG -> CLAIMED -> RED_TEST -> IMPLEMENTED -> SELF_REVIEWED
        -> INTEGRATION_TESTED -> PROFILED_IF_REQUIRED -> DONE
        -> BLOCKED | REJECTED
```

Transitions are recorded in `ledger/events.jsonl`. An agent may claim and
advance implementation states. `DONE` requires:

- all listed tests green;
- no open merge blocker;
- if the task is a scientific comparison, a `gate_result.json` written by
  `gbh gate evaluate`, not by the agent.

## 2. Gate protocol

Each gate is a pure function `pass = f(metrics) -> GateResult`.

The agent writes `metrics.json` only. Evaluation:

```bash
gbh gate evaluate --gate G1_PATCH_QUALITY --metrics path/to/metrics.json
```

The evaluator appends one line to `ledger/gates.jsonl` and writes
`runs/<run_id>/gate_result.json`. Overwriting a prior result for the same
`(gate, run_id)` is refused unless `--supersede` is set and an ADR path is
provided.

Locked GeoByteLab v2 numbers (do not fish):

| Gate | Pass |
|---|---|
| G0_CAUSAL | suffix edits after t do not change logits/boundaries through t |
| G1_PATCH_QUALITY | at mean 4.5–6.0 B/patch, ΔBPB ≤ +0.010 vs strongest comparable baseline |
| G2_PATCH_EFFICIENCY | at matched BPB: +15% raw B/s **or** −20% global KV, local overhead included |
| G3_ENTROPY_VALUE | entropy patcher beats fixed and delimiter on the primary aggregate |
| G5_SPHERE | ≥10% lower wall time to target BPB or supported quality gain; ≤5% step-time penalty |
| G6_PHASE | prime_log beats RoPE **and** every matched spectral control |
| G7_HYP | ≥5% hierarchy-probe gain vs equal-dim Euclidean head; ΔBPB ≤ +0.005 |
| G8_SHEAF | ≥5% consistency-probe gain vs identity/graph controls; ΔBPB ≤ +0.005; graceful at 10% edge noise |
| G9_KOOP | beats param-matched MLP on held-out multi-step latent pred; ΔBPB ≤ +0.005; stable spectrum |
| E6_TRAINER | ΔBPB ≤ +0.005 vs H-Net/patch control **and** ≥10% relative flip-rate drop **and** beats ρ=I |
| E6_DETECTOR | AUROC(sheaf) > max(entropy, max-logit, cosine) |
| E6_RHO_COLLAPSE | RAISE if σ_min(ρ) < 0.1 or effective rank < d/4 |
| E3_TO_E4 | δ_rel(real) ≤ 0.3 **and** ≤ min(nulls) − 0.1 |
| E2_SPHERE | nGPT admitted only if it beats QK-norm |
| E5_HASH | hash/VSA within noise of or better than 256×d byte table |

λ for sheaf trainer ∈ {1e-3, 1e-2} only.

## 3. Toolchain

Required on PATH after `uv sync`:

- Python 3.12
- `uv`, `just`
- `gbh` CLI (this package)
- `ruff`, `pytest`

Late optional, never baseline: `geoopt`, `ripser`, FlashAttention, Mamba,
custom CUDA.

Pinned consumer stack when driving GeoByteLab:

- PyTorch ≥ 2.9.1+cu128 on Linux for sm_120
- SDPA / cuDNN-flash or FlexAttention (no official FA2 wheel for sm_120)
- bf16 on 5070; skip FP8 below ~1B
- Muon (2D) + AdamW (embed/head/1D)

## 4. GPU scheduler

Jobs declare `device_class: train_5070 | aux_1660ti | cpu`.
The runner takes an atomic file lock under `ledger/locks/`, sets
`CUDA_VISIBLE_DEVICES`, records GPU UUID, and releases on exit or stale
heartbeat (default 15 min).

No `device_map="auto"` in confirmatory runs. No heterogeneous DDP.

## 5. Source lock

Non-smoke runs fail closed unless every Hub source is a commit SHA in
`manifests/sources.lock.yaml`.

## 6. Success

The harness succeeds when an agent can implement A00–A13 of GeoByteLab
without writing a gate result by hand and without smuggling Prime Crystal
into the default residual stream.
