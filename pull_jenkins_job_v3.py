import requests
import json
import os
from urllib.parse import urljoin

# Jenkins server details
jenkins_url = 'http://your-jenkins-server'
username = 'your-username'
api_token = 'your-api-token'

# Create a session to persist certain parameters across requests
session = requests.Session()
session.auth = (username, api_token)

def get_all_jobs(folder=''):
    url = f'{jenkins_url}/job/{folder}/api/json' if folder else f'{jenkins_url}/api/json'
    response = session.get(url)
    response.raise_for_status()
    return response.json()

def get_job_config(folder, job_name):
    url = f'{jenkins_url}/job/{folder}/job/{job_name}/config.xml' if folder else f'{jenkins_url}/job/{job_name}/config.xml'
    response = session.get(url)
    response.raise_for_status()
    return response.text

def save_job_config(folder, job_name, config):
    directory = os.path.join('jenkins_jobs', folder.replace('/', '_'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f'{job_name.replace("/", "_")}.xml')
    with open(file_path, 'w') as file:
        file.write(config)

def get_jenkinsfile_content(folder, job_name, branch):
    url = urljoin(jenkins_url, f'/job/{folder}/job/{job_name}/job/{branch}/wfapi/describe')
    response = session.get(url)
    response.raise_for_status()
    data = response.json()
    scm_url = data['scm']['url']
    scm_branch = data['scm']['branch']
    
    # Assuming Jenkinsfile is located at the root of the branch
    jenkinsfile_url = f'{scm_url}/raw/{scm_branch}/Jenkinsfile'
    scm_response = session.get(jenkinsfile_url)
    scm_response.raise_for_status()
    return scm_response.text

def save_jenkinsfile(folder, job_name, branch, jenkinsfile_content):
    directory = os.path.join('jenkins_jobs', folder.replace('/', '_'), job_name.replace('/', '_'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f'{branch}_Jenkinsfile')
    with open(file_path, 'w') as file:
        file.write(jenkinsfile_content)

def fetch_jobs_and_configs(folder=''):
    jobs = get_all_jobs(folder)
    for job in jobs.get('jobs', []):
        if job['_class'] == 'com.cloudbees.hudson.plugins.folder.Folder':
            sub_folder = f'{folder}/job/{job["name"]}' if folder else job['name']
            fetch_jobs_and_configs(sub_folder)
        elif job['_class'] == 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject':
            multibranch_folder = f'{folder}/job/{job["name"]}' if folder else job['name']
            branches = get_all_jobs(multibranch_folder)
            for branch in branches.get('jobs', []):
                branch_name = branch['name']
                jenkinsfile_content = get_jenkinsfile_content(multibranch_folder, job['name'], branch_name)
                save_jenkinsfile(multibranch_folder, job['name'], branch_name, jenkinsfile_content)
                print(f'Saved Jenkinsfile for branch: {branch_name} of job: {job["name"]}')
        else:
            job_name = job['name']
            job_config = get_job_config(folder, job_name)
            save_job_config(folder, job_name, job_config)
            print(f'Saved config for job: {folder}/{job_name}' if folder else f'Saved config for job: {job_name}')

if __name__ == '__main__':
    fetch_jobs_and_configs()
