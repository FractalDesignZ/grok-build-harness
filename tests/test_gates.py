from gbh.gates import evaluate


def test_e6_trainer_three_ands():
    fail = evaluate(
        "E6_TRAINER",
        {
            "delta_bpb_vs_control": 0.001,
            "flip_rate_rel_drop": 0.11,
            "beats_rho_I": False,
        },
    )
    assert fail.passed is False
    ok = evaluate(
        "E6_TRAINER",
        {
            "delta_bpb_vs_control": 0.001,
            "flip_rate_rel_drop": 0.11,
            "beats_rho_I": True,
        },
    )
    assert ok.passed is True


def test_e6_rho_collapse_raises():
    r = evaluate("E6_RHO_COLLAPSE", {"sigma_min": 0.05, "eff_rank": 8, "d": 64})
    assert r.raised is True
    assert r.passed is False


def test_e3_null_margin():
    r = evaluate(
        "E3_TO_E4",
        {
            "delta_rel_real": 0.25,
            "delta_rel_shuf": 0.28,
            "delta_rel_randinit": 0.40,
            "delta_rel_gauss": 0.50,
        },
    )
    assert r.passed is False


def test_e2_does_not_self_pass_ngpt():
    r = evaluate(
        "E2_SPHERE",
        {"steps_or_bpb_qknorm": 1.0, "steps_or_bpb_ngpt": 1.05},
    )
    assert r.metrics["ngpt_admitted"] is False
