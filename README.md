# Evergreen QA: 60-minute practical lab

**SYNTHETIC LEARNING PROJECT. NOT an implementation or QA validation of the UCSF Evergreen Patch Management product.**

Run tests, generate JUnit+Allure evidence, see a pass/fail report, run Playwright against a local UI mock, trigger a GitHub Actions pipeline on push, and optionally import test results to a sandbox Jira Xray Cloud or Zephyr Scale Cloud instance.

## Start here

1. Open [`docs/01_ONE_HOUR_SCRIPT.md`](docs/01_ONE_HOUR_SCRIPT.md) and follow the Windows PowerShell commands.
2. Understand the Jira/report storage boundaries in [`docs/02_JIRA_XRAY_ZEPHYR.md`](docs/02_JIRA_XRAY_ZEPHYR.md).
3. Review the team ownership and six-month practical roadmap in [`docs/03_ROLES_AND_REAL_PROJECT.md`](docs/03_ROLES_AND_REAL_PROJECT.md).
4. See the [architecture diagram and execution flow](docs/06_ARCHITECTURE_AND_FLOW.md).

### Fast path (Windows, Python installed)

```powershell
.\scripts\run-local.ps1
start reports\summary.html
```

### Fast path (macOS/Linux)

```bash
bash scripts/run-local.sh
```

### Optional browser demo

```bash
npm install
npx playwright install chromium
npm run test:ui
```

### How outputs relate

`pytest/Playwright test -> JUnit XML (import to Jira) + Allure raw/Playwright traces (archive in CI) -> Allure HTML (optional) -> Jira execution+link to secure artifacts`.

### Provenance

Lab structure and scenarios were derived from supplied UCSF project documentation: Test and Evaluation Plan DRAFT v0.2; Security and IAM Workbook DRAFT v0.2; State Machine Design Notes v0.2; Technical Implementation Plan v1.6, plus official public Xray, Zephyr, Allure and GitHub Actions integration documentation (links in docs). The toy service is **new teaching code** and cannot substantiate a single UCSF product pass or defect.
