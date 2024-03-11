import subprocess
import os
import requests
import ctypes
import sys
from zipfile import ZipFile


cli_path = 'NOT SET'
if os.name == 'nt':
    cli_path = os.path.join('.', 'arduino-cli', 'windows')
elif os.name == 'posix':
    cli_path = os.path.join('.', 'arduino-cli', 'mac_linux')
    



# installing the arduino-cli
def install_arduino_cli():
    # check if the arduino-cli is installed
    try:
        vercmd = os.path.join(cli_path, 'arduino-cli.exe') + ' version'
        subprocess.run(vercmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        # install the arduino-cli
        # if windows, download the cli exe
        if os.name == 'nt':
            print("Downloading Windows arduino-cli...")
            
            url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
            
            r = requests.get(url)
            with open(os.path.join(cli_path, "arduino-cli.zip"), "wb") as f:
                f.write(r.content)

            # extract the zip file
            with ZipFile(os.path.join(cli_path, "arduino-cli.zip"), 'r') as zip_ref:
                zip_ref.extractall(cli_path)
            
            # remove the zip file and license
            os.remove(os.path.join(cli_path, "arduino-cli.zip"))
            os.remove(os.path.join(cli_path, "LICENSE.txt"))
        elif os.name == 'posix':
            print("Downloading Mac/Linux arduino-cli...")
            
            posixcmd = 'curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=./arduino-cli/mac_linux sh'
            
            # run the command
            subprocess.run(posixcmd, shell=True, check=True)
        else:
            print("OS not supported")
            print("How did you get here?")
            return
        
        

if __name__ == '__main__':
    # install the arduino-cli if not installed
    install_arduino_cli()    
    
    
    
    