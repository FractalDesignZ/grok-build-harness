"""Pure-function scientific gates. Agents submit metrics; this module decides."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GateResult(BaseModel):
    gate: str
    passed: bool
    reason: str
    metrics: dict[str, Any] = Field(default_factory=dict)
    raised: bool = False


def gate_e5_hash(m: dict[str, Any], noise: float = 0.005) -> GateResult:
    h, t = float(m["bpb_hash"]), float(m["bpb_table"])
    passed = h <= t + noise
    return GateResult(
        gate="E5_HASH",
        passed=passed,
        reason="hash/VSA within noise of or better than byte table" if passed else "hash/VSA lost to table",
        metrics=m,
    )


def gate_e1_hnet(m: dict[str, Any]) -> GateResult:
    passed = float(m["flops_hnet"]) <= 0.5 * float(m["flops_bpe"])
    return GateResult(
        gate="E1_HNET",
        passed=passed,
        reason="H-Net FLOPs ≤ 0.5× BPE at matched BPB" if passed else "compute-reduction claim dies",
        metrics=m,
    )


def gate_e2_sphere(m: dict[str, Any]) -> GateResult:
    qk = float(m["steps_or_bpb_qknorm"])
    ngpt = float(m.get("steps_or_bpb_ngpt", qk))
    admit_ngpt = ngpt < qk
    return GateResult(
        gate="E2_SPHERE",
        passed=True,
        reason="nGPT admitted" if admit_ngpt else "sphere pillar collapses to QK-norm",
        metrics={**m, "ngpt_admitted": admit_ngpt},
    )


def gate_e3_to_e4(m: dict[str, Any]) -> GateResult:
    real = float(m["delta_rel_real"])
    nulls = [
        float(m["delta_rel_shuf"]),
        float(m["delta_rel_randinit"]),
        float(m["delta_rel_gauss"]),
    ]
    passed = real <= 0.3 and real <= min(nulls) - 0.1
    return GateResult(
        gate="E3_TO_E4",
        passed=passed,
        reason="tree-like vs nulls; E4 licensed" if passed else "E4 stays unbuilt",
        metrics=m,
    )


def gate_e6_detector(m: dict[str, Any]) -> GateResult:
    sheaf = float(m["auroc_sheaf"])
    ctrl = max(float(m["auroc_entropy"]), float(m["auroc_maxlogit"]), float(m["auroc_cosine"]))
    passed = sheaf > ctrl
    return GateResult(
        gate="E6_DETECTOR",
        passed=passed,
        reason="sheaf AUROC beat cheap controls" if passed else "detector buried by entropy/logit/cosine",
        metrics=m,
    )


def gate_e6_trainer(m: dict[str, Any]) -> GateResult:
    d_bpb = float(m["delta_bpb_vs_control"])
    flip = float(m["flip_rate_rel_drop"])
    beats_i = bool(m["beats_rho_I"])
    passed = d_bpb <= 0.005 and flip >= 0.10 and beats_i
    return GateResult(
        gate="E6_TRAINER",
        passed=passed,
        reason="nontrivial rho rescued consistency from oversmoothing" if passed else "trainer failed one of three ANDs",
        metrics=m,
    )


def gate_e6_rho_collapse(m: dict[str, Any]) -> GateResult:
    sigma_min = float(m["sigma_min"])
    eff_rank = float(m["eff_rank"])
    d = float(m["d"])
    raised = sigma_min < 0.1 or eff_rank < d / 4
    return GateResult(
        gate="E6_RHO_COLLAPSE",
        passed=not raised,
        raised=raised,
        reason="rho collapsed; run invalid" if raised else "rho audit clean",
        metrics=m,
    )


def gate_g0_causal(m: dict[str, Any]) -> GateResult:
    passed = bool(m.get("logits_stable", False)) and bool(m.get("boundaries_stable", False))
    return GateResult(
        gate="G0_CAUSAL",
        passed=passed,
        reason="causal suffix invariant holds" if passed else "leakage detected",
        metrics=m,
    )


def gate_g1_patch_quality(m: dict[str, Any]) -> GateResult:
    passed = float(m["delta_bpb"]) <= 0.010
    return GateResult(
        gate="G1_PATCH_QUALITY",
        passed=passed,
        reason="patch BPB regression within 0.010" if passed else "patch quality miss",
        metrics=m,
    )


def gate_g2_patch_efficiency(m: dict[str, Any]) -> GateResult:
    bps = float(m.get("bytes_per_sec_rel", 1.0))
    kv = float(m.get("kv_rel", 1.0))
    passed = bps >= 1.15 or kv <= 0.80
    return GateResult(
        gate="G2_PATCH_EFFICIENCY",
        passed=passed,
        reason="throughput or KV gate hit" if passed else "no measured efficiency win",
        metrics=m,
    )


REGISTRY: dict[str, Any] = {
    "E5_HASH": gate_e5_hash,
    "E1_HNET": gate_e1_hnet,
    "E2_SPHERE": gate_e2_sphere,
    "E3_TO_E4": gate_e3_to_e4,
    "E6_DETECTOR": gate_e6_detector,
    "E6_TRAINER": gate_e6_trainer,
    "E6_RHO_COLLAPSE": gate_e6_rho_collapse,
    "G0_CAUSAL": gate_g0_causal,
    "G1_PATCH_QUALITY": gate_g1_patch_quality,
    "G2_PATCH_EFFICIENCY": gate_g2_patch_efficiency,
}


def evaluate(gate: str, metrics: dict[str, Any]) -> GateResult:
    if gate not in REGISTRY:
        raise KeyError(f"unknown gate: {gate}")
    return REGISTRY[gate](metrics)
