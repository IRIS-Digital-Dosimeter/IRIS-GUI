from pyduinocli.commands.arduino import ArduinoCliCommand as Arduino
import os
from pprint import pprint
from zipfile import ZipFile


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

    
    
    
    
    