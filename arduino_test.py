import re
import subprocess
import os
import requests
import ctypes
import sys
from zipfile import ZipFile


cli_path = 'NOT SET'
exe_path = 'NOT SET'
if os.name == 'nt':
    cli_path = os.path.join('.', 'arduino-cli', 'windows')
    exe_path = os.path.join(cli_path, 'arduino-cli.exe')
elif os.name == 'posix':
    cli_path = os.path.join('.', 'arduino-cli', 'mac_linux')
    exe_path = os.path.join(cli_path, 'arduino-cli')
    



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
        
# run the arduino-cli with the given arguments
def run_arduino_cli(args: list[str]):
    cmd = exe_path + ' '
    
    for arg in args:
        cmd += arg + ' '
        
    try :
        return subprocess.run(cmd, text=True, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("Error running command: " + cmd)
        print("Error code:\n" + e.stderr)
        
# compile, upload, and verify the sketch at the given path (path should be the .ino file)
def compile_upload_verify(port: str, fqbn: str, sketch_path: str, usbstack='arduino'):
    # verify the path is valid
    if not os.path.exists(sketch_path):
        print("Invalid path")
        # exit(1)
        
    
    # shaboom
    result = run_arduino_cli(['compile', '-p', port, '-b', fqbn + ':usbstack=' + usbstack, sketch_path, '-u', '-t', '--clean'])
    
    return result

# install necessary cores (idk what theyre actually called) for the M0 board
def install_M0_reqs():
    out = []
    
    # install the Adafruit SAMD board library
    out.append(run_arduino_cli(['core', 'install', 'adafruit:samd']))
    
    # install the Adafruit AVR board library
    out.append(run_arduino_cli(['core', 'install', 'adafruit:avr']))
    
    # install the Arduino SAMD board library
    out.append(run_arduino_cli(['core', 'install', 'arduino:samd']))

    # install the Arduino SAM board library
    out.append(run_arduino_cli(['core', 'install', 'arduino:sam']))
    
    # install the Arduino AVR board library
    out.append(run_arduino_cli(['core', 'install', 'arduino:avr']))

    return out

# install libraries
def install_default_libs():
    out = []
    
    # install the RTCZero library
    out.append(run_arduino_cli(['lib', 'install', 'RTCZero']))

    # install the Adafruit NeoPixel library
    out.append(run_arduino_cli(['lib', 'install', '"Adafruit NeoPixel"']))
    
    # install the Adafruit SPIFlash library
    out.append(run_arduino_cli(['lib', 'install', '"Adafruit SPIFlash"']))
    
    # install the Adafruit TinyUSB library
    out.append(run_arduino_cli(['lib', 'install', '"Adafruit TinyUSB Library"']))
    
    # install the Adafruit ZeroDMA library
    out.append(run_arduino_cli(['lib', 'install', '"Adafruit Zero DMA Library"']))
    
    # install the Adafruit LibPrintf library
    out.append(run_arduino_cli(['lib', 'install', '"LibPrintf"']))

    return out

# returns a tuple of the port, FQBN, and core of the first connected board
def get_board_data():
    # check if a string is a valid looking FQBN
    def is_fqbn_valid(fqbn: str):
        # Define a regular expression pattern for the desired format
        pattern = r'^[^\s:]+:[^\s:]+:[^\s:]+$'

        # Use re.match to check if the input string matches the pattern
        match = re.match(pattern, fqbn)
        
        return None if match is None else match.group()
        
    # check if a string is a valid looking core
    def is_core_valid(core: str):
        # Define a regular expression pattern for the desired format
        pattern = r'^[^\s:]+:[^\s:]+$'

        # Use re.match to check if the input string matches the pattern
        match = re.match(pattern, core)
        
        return None if match is None else match.group()


    # get the list of connected boards
    board_list_data = run_arduino_cli(['board', 'list'])

    # split the output by newlines
    entries = board_list_data.stdout.split('\n')
    
    # make sure there's at least 1 connected board
    if len(entries) < 2:
        return None
    
    # just get the first entry
    # entries[0] is the header/labels
    entry = entries[1]
    
    port, FQBN, core = None, None, None
    
    # split the entry by spaces (gets messy)
    entry = entry.split(' ')
    
    # find the port (its the first entry lol)
    # looks like "COM3" or "/dev/ttyACM0"
    port = entry[0]
    
    # find the FQBN (it should look like "xxx:yyy:zzz")
    for j in entry:
        if is_fqbn_valid(j) is not None:
            FQBN = j
            break
        
    # find the core (it should look like "xxx:yyy")
    for j in entry:
        if is_core_valid(j) is not None:
            core = j
            break
        
    return (port, FQBN, core)

    
    

if __name__ == '__main__':
    # install the arduino-cli, board reqs, and lib reqs if not installed
    # install_arduino_cli()
    # install_M0_reqs()
    # install_default_libs()
    
    port, FQBN, core = get_board_data()
    
    print("Port: " + port)
    print("FQBN: " + FQBN)
    print("Core: " + core)
    print('---------------------------------')

    compile_upload_verify(port, FQBN, '"C:\\Users\\SEVAK\\Documents\\GitHub\\IRIS-Project\\sandbox\\M0\\mass storage andrew\\msc_sdfat\\msc_sdfat.ino"', usbstack='tinyusb')
    
    while True:
        # get input and split by space into list
        args = input("Enter command: ").split(' ')
        print(run_arduino_cli(args))
    
    
    
    
    
    
    