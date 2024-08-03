#!/usr/bin/env python

import requests
import base64
import json
from datetime import datetime

#
#date,source_project,source_repo_name,dest_repo_name,dest_gh_org

# Replace these variables with your information
GITHUB_TOKEN = ''
REPO_OWNER = 'ncmuthu'
REPO_NAME = 'testrepo'
FILE_PATH = 'migration_status.txt'
BRANCH = 'main'  # or the branch you want to update

# GitHub API URL for the file
url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

# Get the current content of the file
response = requests.get(url, headers=headers)
response.raise_for_status()
file_info = response.json()
sha = file_info['sha']
content = base64.b64decode(file_info['content']).decode('utf-8')

# Get the current date
current_date = datetime.now()
formatted_date = current_date.strftime('%Y-%m-%d')
#
source_project = "RTCIS"
source_repo_name = "Test repo"
dest_repo_name = "pru-gtesandbox"
dest_gh_org = "pru-gte"

# Content to add
additional_content = f"{formatted_date},{source_project},{source_repo_name},{dest_repo_name},{dest_gh_org}\n"

# Update the content
updated_content = content + additional_content
updated_content_base64 = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

# Prepare the data for the update
data = {
    'message': 'Update file content via API',
    'content': updated_content_base64,
    'sha': sha,
    'branch': BRANCH
}

# Update the file
response = requests.put(url, headers=headers, data=json.dumps(data))
response.raise_for_status()

if response.status_code == 200:
    print("File updated successfully!")
else:
    print(f"Failed to update file. Status code: {response.status_code}")
    print(response.json())
