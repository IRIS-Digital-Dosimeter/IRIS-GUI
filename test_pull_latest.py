import arduino_helper as ah
import requests
import os


# downloads the contents of a specific folder from a github repo
def download_github_folder_contents(repo_user, repo_name, branch_name, folder_path, local_dir):
    # construct the API URL for the specific folder in the repository
    api_url = f'https://api.github.com/repos/{repo_user}/{repo_name}/contents/{folder_path}?ref={branch_name}'

    # set the headers for the request
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    # send a GET request to the GitHub API
    r = requests.get(api_url, headers=headers)
    
    # parse the JSON response to get the file data
    file_data = r.json()
    
    # loop through each file in the folder
    for file in file_data:
        # get the download URL and name for the file
        file_url = file['download_url']
        file_name = file['name']

        # send GET request to download the file
        r = requests.get(file_url)
        
        # open each file in write-binary mode and save it to the local directory
        with open(os.path.join(local_dir, file_name), 'wb') as f:
            f.write(r.content)

repo_user = 'IRIS-Digital-Dosimeter'
repo_name = 'IRIS-Project'
branch_name = 'sandbox_DMA'
folder_path = 'sandbox/testing_scripts/Home/Test8'
local_dir = './test/'

download_github_folder(repo_user, repo_name, branch_name, folder_path, local_dir)
