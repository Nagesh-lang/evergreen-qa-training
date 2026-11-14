# A six-month QA leadership experience compressed into one lab

Do each line once in the lab; then explain what the production equivalent requires. This is practice, **not** accelerated proof of the UCSF platform.

| Real project phase (sequence illustrative; actual milestones require confirmation) | 1-hour lab equivalent | Real deliverable |
|---|---|---|
| Month 1: understand requirements and build a traceability matrix | Open `docs/sample_rtm.csv` and source references | Reviewed RTM, first testable scope, named test owners and environment readiness |
| Month 1–2: build test framework and CI gates | Execute 15 fast tests; examine `.github/workflows/qa-lab.yml` | Source-controlled unit/contract/policy/agent/security suites with build gates |
| Month 2: deploy TEST and execute synthetic E2E | Run synthetic park/resume and seal checks locally | Actual TEST campaign with Step Functions, ledger/seal and stubs, independently validated |
| Month 2–3: handle failures and security | Run intentional failure; inspect evidence and simulated role denial | Failure drills, security route matrix, defects and fixes with verified retests |
| Month 3: demonstrate acceptance and readiness | Run UI demo and inspect read-only auditor | Real persona walkthroughs and seven UAT scenarios with UCSF signoff |
| Month 3–4: report and evidence governance | Generate JUnit, Allure raw, portable HTML and manifest | Durable evidence storage, CI links, import into Jira executions, environment/build traceability |
| Month 4–5: evaluate agent changes | Run toy agent/injection checks, read TEP dataset principles | Governed golden set, scoring/baselines, parity labels and promotion gates |
| Month 5–6: sustain quality | Use weekly rhythm from `03_ROLES_AND_REAL_PROJECT.md` | Nightly regression, risk-based coverage, quarterly drills, flaky test triage, dashboards |

## QA gate checklist for any deployment

1. Is this a code/agent/prompt/policy change? Determine the impacted requirements and affected test layers.
2. Which suite runs before merge and after deployment? Separate local mocks from deployed TEST assertions.
3. What independent oracle proves success? Avoid assertions that repeat the implementation's own decision as expected truth.
4. Which dataset, fixture version, identity and clock were used?
5. Was the run fully executed? Record pass/fail/blocked/skipped and whether a threshold was formally approved.
6. Are source SHA, environment, timestamps, run ID and artifact links stored together?
7. Were failures triaged, reproducible product defects filed, and fixes verified against regression?
8. Did relevant engineering/security/UCSF gate owners approve promotion?

## Difference between rehearsing and actually being ready

The training's one-hour green run shows your ability to operate a toolchain. **It does not validate actual API schemas, deployments, data fidelity, security permissions, AI quality, performance, or UCSF acceptance.** Those require the real approved build, fixtures, environment and evidence.
