"""Optional CLOUD-only JUnit result importer; does nothing without explicit config.

Never hardcode secrets. NEVER run on unapproved production or external data.
Xray Cloud and Zephyr Scale Cloud have different APIs; do not reuse this for Jira DC.
"""
from pathlib import Path
import os
import sys


def main():
    provider = os.getenv('QA_JIRA_PROVIDER', '').strip().lower()
    project = os.getenv('QA_JIRA_PROJECT', '').strip()
    filename = Path(os.getenv('QA_JUNIT_PATH', 'reports/junit.xml'))
    if not provider:
        print('SKIP Jira publication: QA_JIRA_PROVIDER not configured (expected in training).')
        return 0
    if provider not in ('xray', 'zephyr'):
        raise RuntimeError('Use QA_JIRA_PROVIDER=xray or zephyr (Cloud only).')
    if not project:
        print('SKIP Jira publication: QA_JIRA_PROJECT not configured.')
        return 0
    if not filename.exists():
        raise FileNotFoundError(f'Cannot publish: {filename} missing')
    try:
        import requests
    except ImportError as e:
        raise RuntimeError('Install dependency: pip install requests') from e

    if provider == 'xray':
        client = os.getenv('XRAY_CLIENT_ID')
        secret = os.getenv('XRAY_CLIENT_SECRET')
        if not client or not secret:
            print('SKIP Xray publication: XRAY_CLIENT_ID/SECRET not configured.')
            return 0
        # Xray Cloud REST API v2 - NOT the Jira REST API.
        base = 'https://xray.cloud.getxray.app/api/v2'
        auth = requests.post(base + '/authenticate',
                             json={'client_id': client, 'client_secret': secret}, timeout=30)
        auth.raise_for_status()
        token = auth.json()  # Xray returns the token as a JSON-encoded string.
        with filename.open('rb') as report:
            result = requests.post(base + '/import/execution/junit',
                                   params={'projectKey': project}, data=report,
                                   headers={'Authorization': 'Bearer ' + token,
                                            'Content-Type': 'application/xml'}, timeout=60)
    else:
        token = os.getenv('ZEPHYR_API_TOKEN')
        if not token:
            print('SKIP Zephyr publication: ZEPHYR_API_TOKEN not configured.')
            return 0
        # In a test sandbox ONLY, QA_ZEPHYR_AUTOCREATE=true opts in to new test creation.
        autocreate = os.getenv('QA_ZEPHYR_AUTOCREATE','false').lower() == 'true'
        with filename.open('rb') as report:
            result = requests.post('https://api.zephyrscale.smartbear.com/v2/automations/executions/junit',
                                   params={'projectKey':project, 'autoCreateTestCases':str(autocreate).lower()},
                                   files={'file': (filename.name, report, 'application/xml')},
                                   headers={'Authorization':'Bearer '+token}, timeout=60)
    result.raise_for_status()
    # Result may contain execution keys/URLs. Avoid printing credentials, URLs with tokens or request headers.
    print(f'Imported {filename} into {provider.upper()} Cloud project {project}.')
    print('Vendor response:', result.text[:1500])
    print('Allure HTML, screenshots and full evidence remain in restricted CI artifact storage; link run URL in Jira.')
    return 0

if __name__=='__main__':
    sys.exit(main())
