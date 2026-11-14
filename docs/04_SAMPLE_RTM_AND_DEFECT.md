# Practice the missing parts of a six-month QA workflow: RTM, defect, triage and sign-off

The `docs/sample_rtm.csv` below is a teaching example. It is NOT the UCSF requirements traceability matrix.

**RTM:** source requirement -> test ID -> script -> environment -> run ID -> evidence -> pass/fail. Do not infer a real product requirement from synthetic code.

**Defect lifecycle (real product only):** new failure -> check evidence and rerun -> distinguish environment/test defect from product defect -> reproduce using exact build + prerequisites + data -> Jira Bug with expected/actual, impact, trace/log link, severity -> developer fixes -> retest -> regression -> closure or reopen.

Sample Jira Bug text (fictional, do not submit):

- Summary: `[TRAINING ONLY] Mock Ops Center auditor can resume campaign`
- Environment: `local synthetic mock`, no real AWS account
- Build/Commit: `SHA from reports/manifest.json`
- Steps: open mock HTML, leave role as auditor, inspect Resume button
- Expected: button disabled
- Observed: (only if a synthetic lab failure actually occurs)
- Evidence: CI link to `reports/playwright-html/`, screenshot/trace
- Severity: training example, not a product severity
- Link to affected Test: matching automated test identity

**Release gate:** do not say "tested" based on a test being written. Track Designed, Implemented, Executed, Pass/Fail/Blocked/Skipped, Environment, Build SHA, and Evidence URI. A passing mock suite establishes only that the training simulator behaves as its tests expect.
