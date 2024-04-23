import requests
import base64

def create_file_github(owner, repo, file_path, file_content, token):
    # GitHub API URL
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    
    # Encode file content to base64
    base64_content = base64.b64encode(file_content.encode()).decode()

    # Request headers
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Request body
    payload = {
        "message": "Add file via API",
        "content": base64_content
    }

    # Make PUT request to create file
    response = requests.put(api_url, headers=headers, json=payload)

    # Check if request was successful
    if response.status_code == 201:
        print("File created successfully.")
    else:
        print("Failed to create file.")
        print(response.text)

# Example usage
owner = "ncmuthuhome02"
repo = "post-script-test"
file_path = "migration_status.txt"
file_content = "Migrate on::"
token = ""

create_file_github(owner, repo, file_path, file_content, token)
