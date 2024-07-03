
import requests
from requests.auth import HTTPBasicAuth

# Replace these variables with your own values
bitbucket_url = "https://bitbucket.example.com"  # Base URL of your Bitbucket Server
project_key = "PROJECT_KEY"  # Key of the project
repo_slug = "repo_slug"  # Slug of the repository
file_path = "path/to/your/file.txt"  # Path to the file in the repository
branch = "main"  # Branch name
username = "your_username"  # Your Bitbucket Server username
password = "your_password"  # Your Bitbucket Server password or API token

# Construct the URL for the API request
url = f"{bitbucket_url}/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/raw/{file_path}?at={branch}"

# Make the API request
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check the response status code
if response.status_code == 200:
    # Print the content of the file
    print(response.text)
else:
    # Print the error message
    print(f"Error: {response.status_code}")
    print(response.text)
