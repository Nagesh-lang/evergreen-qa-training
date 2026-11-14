#!/usr/bin/env bash
set -uo pipefail
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p reports
python -m pytest tests -m 'not demo_failure and not scale and not acceptance' --junitxml=reports/junit.xml --alluredir=reports/allure-results
status=$?
python scripts/report.py
exit "$status"
