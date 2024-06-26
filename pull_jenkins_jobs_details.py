import requests
import json
import os

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

def get_job_config(job_name):
    url = f'{jenkins_url}/job/{job_name}/config.xml'
    response = session.get(url)
    response.raise_for_status()
    return response.text

def save_job_config(job_name, config):
    directory = 'jenkins_jobs'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f'{job_name.replace("/", "_")}.xml')
    with open(file_path, 'w') as file:
        file.write(config)

def fetch_jobs_and_configs(folder=''):
    jobs = get_all_jobs(folder)
    for job in jobs.get('jobs', []):
        if job['_class'] == 'com.cloudbees.hudson.plugins.folder.Folder':
            fetch_jobs_and_configs(job['name'])
        else:
            job_name = job['name']
            job_config = get_job_config(job_name)
            save_job_config(job_name, job_config)
            print(f'Saved config for job: {job_name}')

if __name__ == '__main__':
    fetch_jobs_and_configs()
