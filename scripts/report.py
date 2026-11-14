"""Portable evidence manifest and simple HTML report, with no extra dependencies.
Allure is richer; this report ensures there is always an inspectable artifact.
"""
import datetime as dt
import html
import json
import os
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

base = Path('reports'); base.mkdir(exist_ok=True)
def git_sha():
    if os.getenv('GITHUB_SHA'): return os.environ['GITHUB_SHA']
    try: return subprocess.check_output(['git','rev-parse','HEAD'], stderr=subprocess.DEVNULL, text=True).strip()
    except Exception: return 'local-unversioned'

runs = []
for report_name in ('junit.xml', 'ui-junit.xml', 'deep-junit.xml'):
    file = base / report_name
    if not file.exists(): continue
    root = ET.parse(file).getroot()
    for tc in root.iter('testcase'):
        status = 'PASS'
        if tc.find('failure') is not None or tc.find('error') is not None: status = 'FAIL'
        elif tc.find('skipped') is not None: status = 'SKIP'
        runs.append({'test': tc.get('classname','')+'.'+tc.get('name',''),
                     'time_seconds':tc.get('time','0'), 'status':status, 'source':report_name})

manifest={'warning':'SYNTHETIC TRAINING DATA. Never present as UCSF product execution or acceptance evidence.',
          'run_id':os.getenv('GITHUB_RUN_ID') or os.getenv('QA_RUN_ID') or 'local-training',
          'sha':git_sha(), 'environment':'LOCAL_SYNTHETIC_TRAINING',
          'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
          'counts':{key:sum(t['status']==key for t in runs) for key in ['PASS','FAIL','SKIP']},
          'junit_test_runs':runs, 'evidence_directory':'reports/evidence',
          'allure_results_directory':'reports/allure-results',
          'retention':'CI artifact retention controlled by repository settings; not permanent by default'}
(base/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
rows=''.join('<tr><td>'+html.escape(t['test'])+'</td><td>'+t['status']+'</td><td>'+t['source']+'</td></tr>' for t in runs)
page=f'''<!doctype html><html><meta charset="utf-8"><title>Evergreen training test run</title>
<style>body{{font:16px Arial;max-width:1050px;margin:36px auto}}.banner{{background:#ffe6a4;padding:14px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:8px;border:1px solid #ddd;text-align:left}}</style>
<h1>Evergreen QA synthetic training run</h1><div class="banner">NOT UCSF PRODUCT VALIDATION. This is a local mock.</div>
<p><strong>Run:</strong> {html.escape(str(manifest['run_id']))} | <strong>SHA:</strong> {html.escape(manifest['sha'])}</p>
<p><strong>Pass:</strong> {manifest['counts']['PASS']} | <strong>Fail:</strong> {manifest['counts']['FAIL']} | <strong>Skip:</strong> {manifest['counts']['SKIP']}</p>
<p>Evidence: <code>reports/evidence/</code>. Detailed metadata: <code>reports/manifest.json</code>. Allure raw data: <code>reports/allure-results/</code>.</p>
<table><thead><tr><th>Test</th><th>Status</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></html>'''
(base/'summary.html').write_text(page,encoding='utf-8')
print('Created reports/manifest.json and reports/summary.html'); print(manifest['counts'])
