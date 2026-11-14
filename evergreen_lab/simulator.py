"""Tiny, deliberately simplified Evergreen-style QA simulator.

SAFETY: Completely fake data; no AWS, UCSF, ServiceNow, BigFix or network calls.
The real product's policy contracts MUST take precedence over this training code.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Witness:
    ci: str
    status: str
    age_minutes: int
    detail: str = ""


def normalize_witness(payload: dict) -> Witness:
    """Illustrative contract - not a substitute for Connector ICD schemas."""
    if not isinstance(payload, dict):
        raise ValueError("witness payload must be an object")
    for field in ("ci", "status", "age_minutes"):
        if field not in payload:
            raise ValueError(f"missing required field: {field}")
    if not isinstance(payload["ci"], str) or not payload["ci"]:
        raise ValueError("invalid ci")
    if payload["status"] not in {"OK", "STALE", "UNKNOWN", "UNAVAILABLE"}:
        raise ValueError("invalid witness status")
    age = payload["age_minutes"]
    if type(age) is not int or age < 0:
        raise ValueError("invalid age_minutes")
    return Witness(payload["ci"], payload["status"], age, str(payload.get("detail", "")))


def decide_gate(witness: Witness, *, kill_switch: bool = False, freshness_minutes: int = 60) -> dict:
    """Synthetic fail-closed logic to exercise testing methodology."""
    if kill_switch:
        return {"result": "PARK", "reason": "KILL_SWITCH"}
    if witness.status != "OK":
        return {"result": "PARK", "reason": "WITNESS_" + witness.status}
    if witness.age_minutes > freshness_minutes:
        return {"result": "PARK", "reason": "STALE_WITNESS"}
    return {"result": "PROCEED", "reason": "CURRENT_WITNESS"}


def campaign_step(state: str, gate: dict, *, explicit_resume: bool = False) -> str:
    if state == "PARKED" and not explicit_resume:
        return "PARKED"
    if gate["result"] == "PARK":
        return "PARKED"
    if state == "PARKED" and explicit_resume:
        return "READY"
    if state in {"NEW", "READY"}:
        return "READY"
    raise ValueError(f"invalid training state {state}")


def authorized(role: str, action: str) -> bool:
    """Subset of role-action examples from Security Workbook section 4.2.
    Full Cedar matrix, conditions and scope checks NOT represented.
    """
    permissions = {
        "patch_ops_engineer": {"read_campaign", "dispose_g1", "resume_park", "kill_switch"},
        "cab_reviewer": {"read_campaign"},
        "security_lead": {"read_campaign", "security_acceptance"},
        "exec_audit": {"read_campaign", "verify_seal"},
        "platform_admin": {"read_campaign", "resume_park", "kill_switch", "admin"},
        "owner_signed_link": {"acknowledge", "request_deferral"},
    }
    return action in permissions.get(role, set())


def tool_gateway(tool_name: str) -> dict:
    allowed = {"read_witness", "read_ledger"}
    return ({"allowed": True, "code": "OK"} if tool_name in allowed
            else {"allowed": False, "code": "DENIED_TOOL"})


def seal_record(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_seal(payload: dict, expected_sha256: str) -> bool:
    return seal_record(payload) == expected_sha256


def model_recommendation(witness: Witness, untrusted_comment: str = "") -> dict:
    """Untrusted text has NO authority over gate decision in this demo."""
    del untrusted_comment
    return {"gate": decide_gate(witness)["result"], "needs_human_review": witness.status != "OK"}


def run_training_campaign(witness: Witness, *, kill_switch: bool = False) -> dict:
    gate = decide_gate(witness, kill_switch=kill_switch)
    state = campaign_step("NEW", gate)
    ledger = [{"event": "gate_decision", "decision": gate, "ci": witness.ci},
              {"event": "campaign_state", "state": state}]
    return {"state": state, "ledger": ledger, "seal": seal_record({"ledger": ledger})}
