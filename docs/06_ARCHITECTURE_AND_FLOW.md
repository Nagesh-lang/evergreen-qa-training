# Architecture and execution flow

> **Synthetic training project only.** These diagrams describe this repository, not the UCSF Evergreen product or its infrastructure.

## Architecture

```mermaid
flowchart LR
    Dev[Developer]

    subgraph Local["Local workstation"]
        RunLocal["run-local.ps1 / run-local.sh"]
        PyTests["pytest tests/"]
        Sim["evergreen_lab/simulator.py"]
        Evidence["Evidence JSON<br/>JUnit XML<br/>Allure raw results"]
        Report["scripts/report.py"]
        Summary["manifest.json<br/>summary.html"]
        Browser["Playwright tests"]
        Mock["ui/mock_ops_center.html<br/>(static local mock)"]
        UiArtifacts["UI JUnit<br/>HTML, screenshots, traces"]
    end

    subgraph CI["GitHub Actions"]
        Triggers["Push / PR / schedule / manual"]
        PyJob["python-fast job"]
        UiJob["ui-smoke job"]
        Archive["Upload reports as artifacts<br/>(including on failure)"]
    end

    Jira["Optional Jira Cloud<br/>Xray OR Zephyr"]

    Dev --> RunLocal --> PyTests
    PyTests --> Sim
    Sim --> Evidence --> Report --> Summary
    Dev --> Browser
    Browser --> Mock
    Browser --> UiArtifacts

    Dev --> Triggers
    Triggers --> PyJob
    Triggers --> UiJob
    PyJob --> PyTests
    PyJob --> Report
    PyJob --> Archive
    UiJob --> Browser
    UiJob --> Archive
    PyJob -. "main push only; explicit config and credentials" .-> Jira
    Archive -. "secure run/artifact link" .-> Jira
```

The Python simulator exercises synthetic witness validation, gate decisions, campaign state, authorization examples, and record sealing. The browser suite opens only the static local mock. Neither test path connects to UCSF or validates a real product.

## QA execution flow

```mermaid
flowchart TD
    Start([Start locally or trigger GitHub Actions])
    Select{Execution path}
    Py["Run pytest against synthetic Python tests"]
    Ui["Run Playwright against the local HTML mock"]
    Sim["Evaluate synthetic gate and campaign behavior"]
    TestOut["Write JUnit XML, evidence JSON, and Allure raw results"]
    UiOut["Write UI JUnit, HTML report, and failure screenshots/traces"]
    MakeReport["Generate manifest.json and summary.html"]
    Allure{"Allure CLI available in CI?"}
    AllureHtml["Generate rich Allure HTML"]
    Archive["Archive generated reports/artifacts<br/>even when tests fail"]
    MainPush{"Push to main?"}
    JiraConfigured{"Jira provider, project, and credentials configured?"}
    Publish["Optionally import JUnit to Xray Cloud or Zephyr Scale Cloud"]
    Skip["Skip Jira publication"]
    End([Review pass/fail results and artifacts])

    Start --> Select
    Select -->|Python| Py --> Sim --> TestOut --> MakeReport
    Select -->|Browser UI| Ui --> UiOut
    MakeReport --> Allure
    Allure -->|Yes| AllureHtml --> Archive
    Allure -->|No| Archive
    UiOut --> Archive
    Archive --> MainPush
    MainPush -->|No| End
    MainPush -->|Yes| JiraConfigured
    JiraConfigured -->|Yes| Publish --> End
    JiraConfigured -->|No| Skip --> End
```

The Python and UI suites are separate CI jobs; the diagram joins them at artifact review to show the overall workflow. Jira import is optional and is only attempted by the workflow on a push to `main`. JUnit carries execution status; detailed evidence remains in the archived reports and artifacts.
