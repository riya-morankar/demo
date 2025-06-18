import json
import os
from datetime import datetime
from openpyxl import Workbook, load_workbook
import subprocess

event_path = os.getenv('GITHUB_EVENT_PATH')
with open(event_path, 'r') as f:
    event = json.load(f)
pr = event.get("pull_request")
if not pr:
    raise ValueError("No pull_request data found.")

req_id = pr.get("number")
title = pr.get("title")
author = pr.get("user", {}).get("login")
source_branch = pr.get("head", {}).get("ref")
action = "Merged" if pr.get("merge_status") == "MERGED" else "Squashed"

comment = pr.get("body")
if not comment:
    comment="N/A"
merged_at = datetime.now().strftime("%Y-%m-%d")

merge_commit_sha = pr.get("merge_commit_sha")
if merge_commit_sha:
    change_id = subprocess.check_output(["git", "show", "-s", "--format=%H", merge_commit_sha]).decode("utf-8").strip()
else:
    change_id = "N/A"
    
excel_file = "new_sheet.xlsx"
if os.path.exists(excel_file):
    wb = load_workbook(excel_file)
    ws = wb.active
else:
    wb = Workbook()
    ws = wb.active
    ws.append(["Source Branch", "Author", "Action", "Comment", "Date", "Change ID"])

ws.append([source_branch, author, action, comment, merged_at, change_id])

wb.save(excel_file)
print(f"Logged new sheet")
