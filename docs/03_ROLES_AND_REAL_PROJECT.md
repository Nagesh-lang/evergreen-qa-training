# How this lab maps to the real six-month Evergreen QA program

## 10-layer implementation RACI (proposed, NOT signed off)

The **owner** shown in TEP §2 is a DOCUMENT DEFINITION OWNER, not necessarily the engineer or team assigned to implement the script.

| Layer | Technical reference | Proposed implementer | QA lead's responsibility | Typical run |
|---|---|---|---|---|
| L1 Unit | Service repos / State Machine Notes | Component developers | Review coverage, critical boundary cases | Each PR/push |
| L2 Contract | Connector ICD §9–10 | Connector developers | Review recorded fixtures, schema expectations | Each PR/push |
| L3 Policy vectors | Policy Authoring Guide §11 | Policy/service developers | Challenge oracles, trace to policies | Each policy change/PR |
| L4 Agent eval | Agent Specs §6 / TEP §4–6 | AI engineers | Govern/inspect parity data, scorecards, false positives and gates | Nightly/version promotion |
| L5 Injection | Agent Specs §7 / Security Workbook §9 | AI/security engineers | Design adversarial cases, check gate isolation | PR of agent/prompt/policy; scheduled |
| L6 Integration | TEP §7 | QA automation with integration developers | Own independent assertions of mock campaign and sealed ledger | TEST promotion smoke/on-demand |
| L7 Scale | TEP §9 | DevOps/performance + QA | Define workloads and verifiable metrics | On scale change / before pilot |
| L8 Failure drills | TEP §8 | QA and DevOps | Verify expected parked state and evidence | Quarterly; read-model rebuild semiannual |
| L9 Security | Security Workbook §10 | Security/platform engineers + QA | Independently verify role/route matrix and configuration | PR/pipeline for auth matrix |
| L10 Acceptance | TEP §11; Cutover Playbook | QA facilitates; UCSF stakeholders execute/sign | Record persona/UAT evidence and defects | Milestone/cutover |

UI Playwright testing crosses L6/L9/L10. It is not an eleventh TEP layer.

## What runs when in a real CI/CD system?

1. **PR / each push:** static checks, unit, connector contract, policy vectors, role matrix checks, selected agent/injection regression; quick mocked UI/API smoke if components exist.
2. **Merge to integration branch:** deploy approved build to TEST (after infrastructure approvals), run state-machine synthetic campaign, seal and ledger assertions, deeper auth/API/UI suites.
3. **Nightly / model or prompt change:** agent eval suite with governed golden datasets and exact model/prompt/policy hashes. Unapproved thresholds must not be falsely turned into go/no-go lines.
4. **Scheduled / release candidate:** failure drills, larger synthetic estate runs, recovery tests, performance, resilience, data-plane verification.
5. **UAT/cutover:** five scripted persona sessions, seven UAT scenarios, acceptance evidence and authorized stakeholder signoff.
6. **Operations:** drift, security and regression monitoring. Quarterly drills; annual/semianual reviews as required by actual runbooks. Update RTM and known risks after each release.

## Document-derived guardrails

- DEV uses synthetic data and mocks. Full synthetic campaign smoke is defined for TEST (TEP Ch.7); scale synthetic estate runs in DEV (Ch.9).
- During Pilot/Shadow, mock/stub any actuator path with real change potential. Do not run live BigFix patch execution or network activation from the lab.
- Security Workbook §4.2 defines multiple role claims and a signed-link owner audience; one Okta login per owner is not an accurate test requirement.
- TEP §11 describes five persona walkthroughs and seven UAT scenarios. This LAB contains only an illustrative persona UI check, not real acceptance.
- TEP §5 says acceptance score floors are illustrative until approved with UCSF.
- The Security Workbook demands default-deny role/action checks and a pipeline scan for no public endpoints; the toy role function in this lab is not Cedar/SCP or a deployed route test.

## Weekly operating rhythm (first six months)

- Monday: evaluate build readiness, access and owners; triage blockers; publish test scope and environment dependencies.
- Daily: monitor CI red builds; classify failures as test defect, environment issue, genuine product defect, data issue or unclear; only real reproduced defects become product bugs.
- Midweek: execute new-component and risk-based regression; inspect evidence completeness; peer-review new test oracles.
- Friday: coverage versus requirements, change-based risk report, defect aging, flaky-test trends, held releases and next-week plan.
- Before each promotion: prove required gates from a build-specific, versioned run; no unexecuted or synthetic-training test can count as acceptance evidence.

## Requests to clarify with Mridul, Tamannah, Sid and Shivam

1. Is Jira Cloud/Server; Xray/Zephyr licenses; who can provision project and API tokens?
2. Which Git host/CI product already exists, and what branch strategy/required checks are approved?
3. Which project code repository/build SHA is QA testing, and what is the first testable scope?
4. Is approved private TEST runner in VPC, through VPN/SSM, or other approved network design?
5. Do synthetic estate, mock connector pack and injectable clock exist now?
6. What evidence storage, access control, data classification and retention does UCSF require?
7. Who is accountable for source test scripts across the 10 layers, and who is the approver for UAT?
8. Confirm the DEV/TEST boundaries, G3 polling-vs-callback contract and IaC baseline.

## Production migration checklist

- [ ] Replace fake simulator with actual API contracts, real service sources and verified business rules.
- [ ] Replace static HTML with actual private Ops Center UI and stable test IDs/selectors.
- [ ] Use approved test roles/identities and signed-link test data; never store credentials in code.
- [ ] Separate secrets and account access by DEV, TEST and PROD; protect deployments.
- [ ] Agree on fixture governance, masking, token revocation, clock API and test cleanup.
- [ ] Validate JUnit → Jira stable ID mapping in sandbox, approve account privileges.
- [ ] Require CI artifact retention and secure evidence links in Test Execution records.
- [ ] Map each acceptance criterion through requirements, tests, executions and evidence.
