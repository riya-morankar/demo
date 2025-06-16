import openpyxl
import os
import json

# Load the Git PR data from the event
event = json.loads(os.environ['GITHUB_EVENT'])

# Create a new Excel workbook
wb = openpyxl.Workbook()

# Get the PR data
pr_data = event['pull_request']

# Create a new sheet for the PR data
sheet = wb.active

# Write the PR data to the sheet
sheet['A1'] = 'PR Title'
sheet['B1'] = pr_data['title']
sheet['A2'] = 'PR Author'
sheet['B2'] = pr_data['user']['login']

# Save the workbook to a file
wb.save('excel-sheet.xlsx')
