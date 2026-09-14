import inspect

from src.execution.local_model_smoke_backend import LocalModelSmokeBackend, ROLE


def test_backend_contract_methods_exist():
    backend = LocalModelSmokeBackend(device="cpu")
    for name in ("pilot", "construct", "qualify", "reattack", "plasticity", "verdict"):
        assert callable(getattr(backend, name))
    assert ROLE == "BENIGN_EXECUTION_SMOKE_ONLY"


def test_backend_does_not_claim_scientific_evidence():
    backend = LocalModelSmokeBackend(device="cpu")
    result = backend._result("pilot", True)
    assert result["scientific_evidence"] is False
    assert result["role"] == ROLE


def test_backend_has_no_formal_attack_method():
    backend = LocalModelSmokeBackend(device="cpu")
    assert not hasattr(backend, "a0")
    assert not hasattr(backend, "a1")
    assert not hasattr(backend, "harmful_evaluator")
