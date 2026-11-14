# Jira, Xray/Zephyr, Allure and CI: what actually happens

## Install and connect (requires Jira admin, correct Cloud/Data Center edition)

1. Jira administrator approves and installs **Xray** OR **Zephyr Scale** from the organization's Jira Marketplace/app governance. Avoid installing both for the same project without a decision.
2. Admin enables project access and grants QA permissions. Create/confirm a Jira project, not a random sandbox in UCSF.
3. Inside the installed app create a **Test** (steps/expected result, or generic test for automation), group into **Test Set/Plan** (Xray) or **Test Cycle/Plan** (Zephyr); link to story/requirement.
4. Configure an API identity/token with minimum rights; keep tokens in CI secret storage. Never paste secrets into scripts, Jira comments or ChatGPT.
5. Run pytest `--junitxml=reports/junit.xml` in CI. Check the `testcase` names don't churn.
6. In CI call `python scripts/publish_jira.py` with appropriate variables. Observe the new Test Execution or Cycle in Jira. Manually link the full secure CI run URL for attachments/screenshots/Allure and include the build SHA.
7. Rerun a test; confirm it is the SAME logical test ID but a NEW execution result for a new build. Avoid duplicate test issues.

**This training ZIP does not connect to Jira by default.** Publication is disabled until the provider and credentials are explicitly configured. Vendor API configuration requires administrator approval.

## Xray Cloud import via JUnit

- Environment variables: `QA_JIRA_PROVIDER=xray`, `QA_JIRA_PROJECT=YOURKEY`, `XRAY_CLIENT_ID`, `XRAY_CLIENT_SECRET`.
- Xray REST v2 authenticates at `https://xray.cloud.getxray.app/api/v2/authenticate` and accepts JUnit at `/api/v2/import/execution/junit`.
- Cloud JUnit importer typically matches generic Test identities by stable `classname + name`. It can create tests on first import, so validate deduplication, scopes and existing test mapping in a sandbox before using company Jira.
- Xray also supports the Xray JSON format to explicitly bind results to existing Jira Test issue keys and richer execution structures; use that later if required.
- The Xray **Server/Data Center** API is different. Do not run Cloud uploader against DC.

## Zephyr Scale Cloud import via JUnit

- Environment variables: `QA_JIRA_PROVIDER=zephyr`, `QA_JIRA_PROJECT=YOURKEY`, `ZEPHYR_API_TOKEN`.
- JUnit upload endpoint: `https://api.zephyrscale.smartbear.com/v2/automations/executions/junit`.
- Zephyr matches known tests by key embedded in test name (e.g. TEST-T1 as `TEST_T1`) or qualified name; missing mappings can error.
- The script defaults `autoCreateTestCases=false`. **For a Jira training sandbox only**, opt in explicitly via `QA_ZEPHYR_AUTOCREATE=true` to create missing tests. Avoid uncontrolled creation in production Jira.
- Confirm whether the installed app is **Zephyr Scale** vs another Zephyr edition; their APIs differ.

## What is stored where?

| Output | What it is | Suggested home |
|---|---|---|
| `junit.xml` | Per-test execution status, durations, failure messages | CI artifact; imported execution summary in Xray/Zephyr |
| `allure-results/` | JSON result and attachments from Allure pytest adapter | Private CI artifact storage |
| `allure-report/` | Interactive generated HTML report (requires Allure CLI) | Private artifact storage / approved static hosting |
| `playwright-html/`, `playwright-results/` | UI screenshots, traces, HTML and JUnit | Restricted CI artifact storage |
| `manifest.json` | Run ID, SHA, environment, timestamp, counts | Keep with every evidence bundle |
| Jira Test / Test Execution / Cycle | Test identity, case steps, execution status, requirement link | Jira (Xray/Zephyr) |
| Jira Bug | Confirmed real product defect, linked to failing execution | Jira issue tracker |

JUnit XML does not natively carry full Allure HTML or external attachments. Standard imports do not mean each screenshot/trace is automatically uploaded as a Jira attachment. Link the secure artifact or explicitly implement an approved attachment integration.

Retention and compliance: CI artifacts expire according to platform settings; select S3/Object Lock, immutable audit evidence or other approved long-term evidence storage only after security and data retention policies are agreed. Never put PHI, credentials or live customer content into public reports.

## Link example

Requirement `EVG-REQ-123` (fictional) → Test `EVG-T55` (fictional) → run `4567`, SHA `abc123` → Jira Test Execution `EVG-EX12` (fictional) → secure CI evidence URL → Jira Bug `EVG-901` (if a *real*, reproduced product failure).

## Official documentation (check your edition)

- Xray Cloud execution imports: https://getxraydocs.atlassian.net/wiki/spaces/XRAYCLOUD/pages/44577176
- Xray Generic test mapping: https://getxraydocs.atlassian.net/wiki/spaces/XRAYCLOUD/pages/44565229
- Zephyr pytest integration: https://support.smartbear.com/zephyr/docs/en/test-automation/pytest-integration.html
- Allure mechanics: https://allurereport.org/docs/how-it-works/
- GitHub artifact docs: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
