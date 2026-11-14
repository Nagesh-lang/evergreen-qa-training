# Your 60-minute hands-on exercise (Windows PowerShell)

> Entire lab is illustrative. You are NOT accessing or validating UCSF infrastructure. Do NOT label these results as product tests.

## 00–10 minutes: run 14+ tests on your laptop

1. Unzip to `C:\Evergreen_QA_60_Minute_Lab` (short path recommended).
2. Open the folder in VS Code; Terminal → New Terminal → PowerShell.
3. Run:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m pytest tests -m 'not demo_failure and not scale and not acceptance' --junitxml=reports/junit.xml --alluredir=reports/allure-results -v
   .\.venv\Scripts\python.exe scripts/report.py
   start reports\summary.html
   ```

**See:** tests passed, `reports/junit.xml`, `reports/allure-results/`, `reports/evidence/`, `reports/manifest.json`, and HTML summary.

If Python is not available, install it using the approved company process. `python` may work instead of `py -3`.
If `allure-pytest` cannot be installed due to network policy, run pytest without `--alluredir`; you can still generate JUnit and the simple report.

## 10–20 minutes: create a RED pipeline and prove failure evidence

Run the intentional failure (expected non-zero return code):

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_intentional_failure.py -m demo_failure --junitxml=reports/junit.xml --alluredir=reports/allure-results -v
.\.venv\Scripts\python.exe scripts/report.py
start reports\summary.html
```

Observe one **FAIL** and a pytest failure reason. This is NOT a defect in UCSF software. Rerun the good suite from step 1 to restore green status.

> Each rerun overwrites `reports/junit.xml`. Clear or archive `reports/allure-results` between independent launches; Allure may merge raw results otherwise.

## 20–30 minutes: run the Playwright TypeScript UI demonstration

Requires Node.js/npm and browser download permission. The UI page is a static, local mock.

```powershell
npm install
npx playwright install chromium
npm run test:ui
npx playwright show-report reports/playwright-html
```

Look at `tests-ui/ops-center.spec.ts`. First test verifies auditor's resume button is disabled. Second verifies the patch operations role can explicitly resume (local mock only).
If the browser cannot be installed in this hour, read the spec and continue; your Python lab is independent.

## 30–40 minutes: generate the rich Allure HTML report

Allure's commandline utility needs Java. If Java 17+ and Node.js are installed:

```powershell
npm install
npm run report:allure
npx allure open reports/allure-report
```

`allure-pytest` writes raw JSON/attachments; the commandline transforms those files into an HTML site. Without Java, `reports/summary.html` remains a usable fallback.

## 40–50 minutes: push the lab to YOUR OWN approved training repository

Create a new empty repository (e.g., `evergreen-qa-training`) on an approved Git hosting service. Do not push UCSF private docs or secrets to a personal/public repository.

```powershell
git init
git add .
git commit -m "Add synthetic Evergreen QA training lab"
git branch -M main
git remote add origin https://github.com/YOUR_APPROVED_ORG/evergreen-qa-training.git
git push -u origin main
```

The `.github/workflows/qa-lab.yml` file creates GitHub Actions jobs on push, PR, schedule, and manual dispatch. On GitHub open **Actions → Evergreen SYNTHETIC QA training → Run → Artifacts**.

GitHub Actions is the teaching example; confirm the real team's Git provider and pipeline orchestrator. If it is Jenkins/GitLab/Bitbucket, translate the same stages rather than creating a second unauthorized pipeline.

## 50–60 minutes: understand Jira integration and rehearse Monday

Read `docs/02_JIRA_XRAY_ZEPHYR.md` and `docs/03_ROLES_AND_REAL_PROJECT.md`.

- Identify whether Jira Cloud or Data Center is used.
- Identify whether Xray/Zephyr is installed (ask your Jira admin if no access).
- Explain why JUnit XML contains status, while Allure and CI artifacts hold detailed evidence.
- Explain mapping: `classname+name` for Xray's Generic Test; Zephyr may match test case key or fully-qualified test name.
- Point to `scripts/publish_jira.py` and name required *secret environment variables*.
- Explain why **hosted GitHub Actions can run this simulator but not private UCSF TEST endpoints** without approved connectivity.

### 90-second rehearsal

> When the developer pushes code, our CI runs unit/contract/policy and security checks. We also run a small smoke suite on pull requests. The runner produces JUnit results and Allure evidence linked to the exact commit SHA. We archive the evidence on both passes and failures. Xray or Zephyr imports the status into Jira Test Executions/Cycles, and we link full artifacts to the run. Test, drill and full acceptance runs require the right TEST environment, secured network access, approved fixtures and responsible owners. I will prove one end-to-end import with Sid and the Jira admin before treating the integration as live.

## Extra 3-minute rehearsal: visualize Jira mapping without an account

```powershell
.\.venv\Scripts\python.exe scripts/preview_jira_import.py --provider xray --project TRAIN
.\.venv\Scripts\python.exe scripts/preview_jira_import.py --provider zephyr --project TRAIN
```

Open `reports/jira-import-preview-xray.json` and `reports/jira-import-preview-zephyr.json`. This is the **test identity mapping you would be publishing**, not a real Jira import.
