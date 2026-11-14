"""Dry-run illustration of how JUnit test results become Jira test executions.
NO NETWORK CALLS OR ACTUAL JIRA WRITES.
"""
import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

p=argparse.ArgumentParser()
p.add_argument('--provider', choices=['xray','zephyr'], default='xray')
p.add_argument('--project',default='TRAIN')
p.add_argument('--junit',default='reports/junit.xml')
args=p.parse_args()
root=ET.parse(args.junit).getroot()
entries=[]
for elem in root.iter('testcase'):
    name=elem.get('name','')
    classname=elem.get('classname','')
    if elem.find('failure') is not None or elem.find('error') is not None: status='FAIL'
    elif elem.find('skipped') is not None: status='SKIP'
    else: status='PASS'
    if args.provider=='xray':
        mapping='Generic Test Definition: '+classname+'.'+name
    else:
        key=re.search(r'\b'+re.escape(args.project)+r'_T\d+\b',name)
        mapping=('Explicit test key: '+key.group(0).replace('_','-')) if key else 'Qualified name: '+classname+'.'+name
    entries.append({'test':classname+'.'+name,'status':status,'proposed_match':mapping})
out={'warning':'DRY RUN ONLY: not uploaded to Jira; not UCSF product evidence',
     'provider':args.provider,'example_project':args.project,
     'jira_execution':'NOT CREATED', 'tests':entries}
path=Path('reports/jira-import-preview-'+args.provider+'.json')
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(out,indent=2), encoding='utf-8')
print(f'{len(entries)} synthetic cases mapped for {args.provider} (DRY RUN). See {path}')
for row in entries[:4]:
    print(' ',row['status'],row['proposed_match'])
