from pyduinocli.commands.arduino import ArduinoCliCommand as Arduino
from pprint import pprint
from zipfile import ZipFile
from pathlib import Path
from zipfile import ZipFile
import os, requests


# cli_path = 'NOT SET'
# exe_path = 'NOT SET'
# if os.name == 'nt':
#     cli_path = os.path.join('.', 'arduino-cli', 'windows')
#     exe_path = os.path.join(cli_path, 'arduino-cli.exe')
# elif os.name == 'posix':
#     cli_path = os.path.join('.', 'arduino-cli', 'mac_linux')
#     exe_path = os.path.join(cli_path, 'arduino-cli')

class BoardStruct:
    def __init__(self, name:str = None, fqbn:str = None, port:str = None, sn:str = None):
        self.__name = name
        self.__fqbn = fqbn
        self.__port = port
        self.__serial_number = sn
        
    @property
    def name(self):
        return self.__name
    
    @property
    def fqbn(self):
        return self.__fqbn
    
    @property
    def port(self):
        return self.__port
    
    @property
    def serial_number(self):
        return self.__serial_number
    
    @property
    def hardware_id(self):
        return self.__serial_number
    
    def __repr__(self):
        return (
            f"Name: {self.name}\n"
            f"FQBN: {self.fqbn}\n"
            f"Port: {self.port}\n"
            f"Serial Number: {self.serial_number}"
        )

class ExtendoArduino(Arduino):   
    __FORMAT_JSON = 'json'
    LIB_DIR = Path(__file__).resolve().parent
    DEFAULT_CLI_TOOL_DIR = Path(LIB_DIR, 'arduino-cli').resolve()
    CLI_YAML_PATH = Path(DEFAULT_CLI_TOOL_DIR, 'arduino-cli.yaml').resolve()
    CLI_DATA_PATH = Path(DEFAULT_CLI_TOOL_DIR, 'data').resolve()
    CLI_USER_PATH = Path(DEFAULT_CLI_TOOL_DIR, 'user').resolve()

    # Modified the original pyduino constructor. There might be a cleaner way
    # to accomplish this but it works for now.
    def __init__(self, additional_urls=None, log_file=None, log_format=None, log_level=None, no_color=None, timeout='300s'):
        """
        :param cli_path: The :code:`arduino-cli` command name if available in :code:`$PATH`. Can also be a direct path to the executable
        :type cli_path: str
        :param config_file: The path to the :code:`arduino-cli` configuration file to be used
        :type config_file: str or NoneType
        :param additional_urls: A list of URLs to custom board definitions files
        :type additional_urls: list or NoneType
        :param log_file: A path to a file where logs will be stored
        :type log_file: str or NoneType
        :param log_format: The format the logs will use
        :type log_format: str or NoneType
        :param log_level: The log level for the log file
        :type log_level: str or NoneType
        :param no_color: Disable colored output
        :type no_color: bool or NoneType
        :param timeout: Timeout for downloads. Must be parseable by https://pkg.go.dev/time#ParseDuration
        :type timeout: str
        """
        
        
        # check if the CLI has already been downloaded/installed locally
        linux_cli_exists = os.path.isfile(os.path.join(ExtendoArduino.DEFAULT_CLI_TOOL_DIR, 'arduino-cli'))
        win_cli_exists = os.path.isfile(os.path.join(ExtendoArduino.DEFAULT_CLI_TOOL_DIR, 'arduino-cli.exe'))
        local_cli_exists = linux_cli_exists or win_cli_exists
        
        # if the CLI exists, set cli_path to the proper path
        # else, download the CLI and assin cli_path to the downloaded path
        if local_cli_exists:
            if os.name == 'nt':
                exec_name = 'arduino-cli.exe'
            elif os.name == 'posix':
                exec_name = 'arduino-cli'
            else:
                raise Exception("OS not supported :(")
            cli_path = os.path.join(ExtendoArduino.DEFAULT_CLI_TOOL_DIR.as_posix(), exec_name)
        else:
            cli_path = self.__install_arduino_cli(ExtendoArduino.DEFAULT_CLI_TOOL_DIR.as_posix())
            
            
        # set the path for the CLI's YAML config file
        config_file = ExtendoArduino.CLI_YAML_PATH.as_posix()
        
        # now we can call the superclass constructor to do the heavy lifting
        super().__init__(
            cli_path=cli_path,
            config_file=config_file,
            additional_urls=additional_urls,
            log_file=log_file,
            log_format=log_format,
            log_level=log_level,
            no_color=no_color,
        )
        
        # if the config file doesn't exist, create it
        if not os.path.isfile(config_file):
            self.config.init(dest_file=config_file)
            
        # set the data and user directory in the config file
        self.config.set('directories.data', [ExtendoArduino.CLI_DATA_PATH.as_posix()])
        self.config.set('directories.user', [ExtendoArduino.CLI_USER_PATH.as_posix()])
        self.config.set('network.connection_timeout', [timeout])
             
    # install necessary cores (idk what theyre actually called) for the M0 board
    # returns output of the command ig
    def install_cores(self):
        print("installing cores")
        cores = [
            'adafruit:samd',
            'arduino:samd',
        ]
        return self.core.install(cores)
    
    # install libraries
    def install_default_libs(self):
        print("installing libs")
        libs = [
            'RTCZero',
            'SdFat - Adafruit Fork',
            'Adafruit TinyUSB Library',
        ]
        
        return self.lib.install(libs)

    # compile, upload, and verify the sketch at the given path (path should be the .ino file)
    def compile_upload_verify(self, port: str, fqbn: str, sketch_path: str, usbstack='arduino'):
        if not os.path.exists(sketch_path):
            raise FileNotFoundError(f"Sketch '{sketch_path}'doesn't exist!")
        
        return self.compile(
            sketch=sketch_path, 
            port=port, 
            fqbn=f"{fqbn}:usbstack={usbstack}",
            verify=True,
            upload=True,
            clean=True
        )

    # returns a list of tuples of the port, FQBN, and core of all connected boards
    # TODO make this function actually useful - maybe fully extract FQBN and Board Name and Port
    def get_board_data(self):
        boards = []
        raw_boards = self.board.list()['result']['detected_ports']
        
        for board in raw_boards:
            name = board["matching_boards"][0]["name"]
            fqbn = board["matching_boards"][0]["fqbn"]
            port = board["port"]["address"]
            sn   = board["port"]["hardware_id"]

            boards.append(BoardStruct(name, fqbn, port, sn))

        return boards

    # installing the arduino-cli
    def __install_arduino_cli(self, path: str) -> str:
        import subprocess
        
        # install the arduino-cli
        # if windows, download the cli exe
        if os.name == 'nt':
            print("Downloading Windows arduino-cli...")
            
            try:
                os.mkdir(path)
            except FileExistsError:
                print('folder exists!')
            
            url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
            
            r = requests.get(url)
            with open(os.path.join(path, "arduino-cli.zip"), "wb") as f:
                f.write(r.content)

            # extract the zip file
            with ZipFile(os.path.join(path, "arduino-cli.zip"), 'r') as zip_ref:
                zip_ref.extractall(path)
            
            # remove the zip file and license
            os.remove(os.path.join(path, "arduino-cli.zip"))
            os.remove(os.path.join(path, "LICENSE.txt"))
            return os.path.join(path, 'arduino-cli.exe')
            
        elif os.name == 'posix':
            print("Downloading Mac/Linux arduino-cli...")

            try:
                os.mkdir(path)
            except FileExistsError:
                # print('Folder exists!')
                pass
            
            posixcmd = f'curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR={path} sh'
            
            # run the install script
            subprocess.run(posixcmd, shell=True, check=True)
            return os.path.join(path, 'arduino-cli')
        else:
            raise SystemError("OS not supported.")
        

    
    
    
    