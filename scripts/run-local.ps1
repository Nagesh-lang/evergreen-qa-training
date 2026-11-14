# Run from the extracted project folder in PowerShell (Windows)
$ErrorActionPreference = 'Stop'
if (!(Test-Path .venv)) { py -3 -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
New-Item -Force -ItemType Directory reports | Out-Null
& .\.venv\Scripts\python.exe -m pytest tests -m 'not demo_failure and not scale and not acceptance' --junitxml=reports/junit.xml --alluredir=reports/allure-results
$testExit = $LASTEXITCODE
& .\.venv\Scripts\python.exe scripts/report.py
Write-Host 'Open reports\summary.html in your browser. For richer Allure reporting, install npm/Java and run npm run report:allure.'
exit $testExit
