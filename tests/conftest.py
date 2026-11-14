from __future__ import annotations
import datetime
import json
import os
from pathlib import Path
import re
import pytest

try:
    import allure
except ImportError:
    allure = None


@pytest.fixture
def evidence(request):
    """Attach safe synthetic observed/expected records for inspection."""
    def emit(name: str, actual, expected):
        run = os.getenv("QA_RUN_ID", "local-training")
        folder = Path("reports/evidence")
        folder.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^a-zA-Z0-9_.-]+", "_", request.node.nodeid)
        path = folder / (slug + "_" + re.sub(r"\W+", "_", name) + ".json")
        payload = {"warning": "SYNTHETIC TRAINING; not UCSF product evidence",
                   "run": run, "test": request.node.nodeid, "note": name,
                   "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "actual": actual, "expected": expected}
        doc = json.dumps(payload, indent=2, default=str)
        path.write_text(doc, encoding="utf-8")
        if allure is not None:
            allure.attach(doc, name=name, attachment_type=allure.attachment_type.JSON)
    return emit


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    folder = Path("reports/evidence")
    folder.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-zA-Z0-9_.-]+", "_", item.nodeid)
    record = {"warning": "SYNTHETIC TRAINING; not UCSF product evidence",
              "run": os.getenv("QA_RUN_ID", "local-training"), "test": item.nodeid,
              "outcome": report.outcome,
              "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (folder / (slug + "_outcome.json")).write_text(json.dumps(record, indent=2), encoding="utf-8")
