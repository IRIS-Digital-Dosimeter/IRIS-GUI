import arduino_helper as ah
import requests
import os
from datetime import datetime


# downloads the contents of a specific folder from a github repo
# returns the path to the folder where the files are saved
def download_github_folder_contents(repo_user, repo_name, branch_name, folder_path, save_dir):
    # construct the API URL for the specific folder in the repository
    api_url = f'https://api.github.com/repos/{repo_user}/{repo_name}/contents/{folder_path}?ref={branch_name}'

    # set the headers for the request
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    # send a GET request to the GitHub API
    r = requests.get(api_url, headers=headers)
    
    # parse the JSON response to get the file data
    file_data = r.json()
    
    
    # check if response dictinoary has key 'message'
    if 'message' in file_data :
        raise Exception('GitHub path or branch may be invalid.')
    
    # create a folder name based on the current date and time as a default value
    folder_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else: 
        print(f'The dir {save_dir} exists')    
        
        
    # loop through each file to create the proper folder name
    for file in file_data:
        # get the file name
        file_name = file['name']
        
        # if `file` is the .ino, create a folder name (same as file_name without the extension)
        splitted = file_name.split('.')
        if splitted[1] == 'ino':
            # - issue there are typically two files with .ino 
            if 'helper' not in splitted[0].lower():
                folder_name = splitted[0]
        
    if not os.path.exists(os.path.join(save_dir, folder_name)):
        os.makedirs(os.path.join(save_dir, folder_name))
    else: 
        print(f'The dir {os.path.join(save_dir, folder_name)} exists')    

    # loop through each file in the folder, this time to save
    for file in file_data:
        # get the download URL and name for the file
        file_url = file['download_url']
        file_name = file['name']

        # send GET request to download the file
        r = requests.get(file_url)
        
        # open each file in write-binary mode and save it to the local directory
        with open(os.path.join(save_dir, folder_name, file_name), 'wb') as f:
            f.write(r.content)
            
    return os.path.join(save_dir, folder_name)








# get the board data and list it
boards = ah.get_board_data()
print('found boards:')
for n, board in enumerate(boards):
    print(f'{n}.', board)

# pick the right board manually :(
board_num = int(input('Enter the number of the board to use: '))
port, FQBN, core = boards[board_num]
print(boards[board_num])

# upload the sketch to the board
repo_user = 'IRIS-Digital-Dosimeter'
repo_name = 'IRIS-Project'
saveto = './test/'

branch_name = 'binary_sdFat'
gitpath = 'sandbox/M0/SdFat/datalogger_tAv_bin'
# download the contents of the datalogger and get the path it was saved to
# datalogger_path = download_github_folder_contents(repo_user, repo_name, branch_name, gitpath, saveto)
datalogger_path = os.path.join('.', 'test', 'datalogger_tAv_bin_DEMO')

branch_name = 'sandbox_DMA'
gitpath = 'sandbox/M0/mass storage andrew/msc_sdfat'
# download the contents of the SD exposer and get the path it was saved to
SD_path = download_github_folder_contents(repo_user, repo_name, branch_name, gitpath, saveto)

print(f'Uploading sketch "{datalogger_path}" to {port} using {FQBN}')
ah.compile_upload_verify(port, FQBN, datalogger_path, usbstack='tinyusb')

input("Press Enter once the datalogger is done creating files!")


boards = ah.get_board_data()
print('found boards:')
for n, board in enumerate(boards):
    print(f'{n}.', board)

# pick the right board manually :(
board_num = int(input('Enter the number of the board to use: '))
port, FQBN, core = boards[board_num]
print(boards[board_num])


print(f'Uploading sketch "{SD_path}" to {port} using {FQBN}')
ah.compile_upload_verify(port, FQBN, SD_path, usbstack='tinyusb')