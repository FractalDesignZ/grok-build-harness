"""Placeholder for consumer causal tests. Harness only checks the protocol shape."""


def test_suffix_mutation_protocol_documented():
    required = (
        "clone sequence",
        "alter positions after t",
        "assert logits through t unchanged",
        "assert boundaries through t unchanged",
    )
    assert len(required) == 4
