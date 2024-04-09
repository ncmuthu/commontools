import requests

# Set Bitbucket Server base URL and credentials
BITBUCKET_BASE_URL = "https://your-bitbucket-server.com"
BITBUCKET_USERNAME = "your-username"
BITBUCKET_PASSWORD = "your-password"

# Set project key
project_key = "your-project-key"

# Construct URL for repositories endpoint
url = f"{BITBUCKET_BASE_URL}/rest/api/1.0/projects/{project_key}/repos"

# Set authentication credentials
auth = (BITBUCKET_USERNAME, BITBUCKET_PASSWORD)

try:
    # Send GET request to Bitbucket Server API
    response = requests.get(url, auth=auth)
    
    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response
        repositories = response.json()["values"]
        
        # Print repository details
        for repo in repositories:
            repo_name = repo["name"]
            owner_name = repo["project"]["key"]
            print(f"Repository Name: {repo_name}, Owner: {owner_name}")
    else:
        # Print error message if request was not successful
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")
except Exception as e:
    # Print exception message if an error occurs
    print(f"An error occurred: {e}")
