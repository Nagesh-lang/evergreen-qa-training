"""Run ONLY on purpose with: python -m pytest -m demo_failure"""
import pytest

@pytest.mark.demo_failure
def test_DEMO_failure_teaches_red_pipeline():
    assert "PARKED" == "READY", "INTENTIONAL FAILURE: demonstrates a red CI run and evidence retention"
