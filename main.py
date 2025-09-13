import pyduinocli
import arduino_helper as a_h
import sys
import subprocess
import crossfiledialog
from pathlib import Path
from pprint import pprint

def main():
    
    
    # install the arduino-cli, board reqs, and lib reqs if not installed
    # also sets up the config file usage and assigns the proper working directories for the CLI tool
    ardu = a_h.ExtendoArduino(
        additional_urls=['https://adafruit.github.io/arduino-board-index/package_adafruit_index.json'],
        timeout='600s'
    )
    
    # out = ardu.install_cores()
    # print('M0 reqs installed')
    
    # # install the default libraries
    # out = ardu.install_default_libs()
    # print('Default libs installed')
    
    # get the list of boards and print them
    boards = ardu.get_board_data()
    # print('found boards:')
    # for n, board_deets in enumerate(boards):
    #     print('---------------------------------')
    #     print(f"{n}:")
    #     print(board_deets)
    #     print('---------------------------------')
    #     print()

    # # pick the right board manually :
    # board_num = int(input('Enter the number of the board to use: '))
    # sel_board = boards[board_num]
    # # port, FQBN, core = boards[board_num]
    
    # print("Selected Board:")
    # print('---------------------------------')
    # print(sel_board)
    # print('---------------------------------')
    

    # da_path = "/home/paelen/Documents/GitHub/IRIS-Project/packages/M0/Binary Serial Logger/serial_log/serial_log.ino"
    # da_path = "C:\\Users\\Sevak\\Documents\\GitHub\\IRIS-Project\\packages\\M0\\Binary Serial Logger\\serial_log\\serial_log.ino"

    # da_path = Path(crossfiledialog.open_file(title="Select an Arduino sketch (.ino) file", filter="*.ino")).resolve()
    # da_path = Path("C:\\Users\\Sevak\\Documents\\GitHub\\IRIS-Project\\packages\\M0\\Binary Serial Logger\\serial_log\\serial_log.ino").resolve()
    sketches = {
        "serial": (Path.home() / "Documents" / "GitHub" / "IRIS-Project" / "packages" / "M0" / "Binary Serial Logger" / "serial_log" / "serial_log.ino").resolve(),
        "tri": (Path.home() / "Documents" / "GitHub" / "IRIS-Project" / "packages" / "M0" / "Triangle Wave Generator" / "triangle_wave_generator" / "triangle_wave_generator.ino").resolve(),
        "logger": (Path.home() / "Documents" / "GitHub" / "IRIS-Project" / "packages" / "M4" / "M4 Datalogger" / "dma_dual_adc_unified_SdFat" / "dma_dual_adc_unified_SdFat.ino").resolve(),
    }
    
    if sys.argv[1] not in sketches.keys():
        print("invalid sketch")
        exit()
    
    des_sketch = sketches[sys.argv[1]].as_posix()


    if sys.argv[1] == "serial":
        if "Adafruit Feather M4 Express (SAMD51)" not in [b.name for b in boards]:
            print("AH")
            exit()


        for b in boards:
            if b.name == "Adafruit Feather M4 Express (SAMD51)":
                sel_board = b
        
        out = ardu.compile_upload_verify(
            port=sel_board.port,
            fqbn=sel_board.fqbn,
            sketch_path=des_sketch
        )
        cmd = [
            sys.executable,
            (Path.home() / "Documents" / "GitHub" / "IRIS-Project" / "packages" / "M0" / "Binary Serial Logger" / "serial_importer_all_in_one" / "serial_importer_all_in_one.py").as_posix(),
            "--plot",
            f"port={sel_board.port}",
            "baud=9600",
            "sec=20",
            "hz=10",
        ]
        print(" ".join(cmd))
        result = subprocess.run(cmd)

        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        
        
    if sys.argv[1] == "tri":
        if "Adafruit Feather M0 (SAMD21)" not in [b.name for b in boards]:
            exit()
        
        for b in boards:
            if b.name == "Adafruit Feather M0 (SAMD21)":
                sel_board = b
    
        out = ardu.compile_upload_verify(
            port=sel_board.port,
            fqbn=sel_board.fqbn,
            sketch_path=des_sketch
        )
        print("tri uploaded")
        
    if sys.argv[1] == "logger":
        if "Adafruit Feather M4 Express (SAMD51)" not in [b.name for b in boards]:
            exit()
        
        for b in boards:
            if b.name == "Adafruit Feather M4 Express (SAMD51)":
                sel_board = b
    
        out = ardu.compile_upload_verify(
            port=sel_board.port,
            fqbn=sel_board.fqbn,
            sketch_path=des_sketch
        )
        
    # print(out)
    
    # try:
    #     out = ardu.compile_upload_verify(
    #         port=sel_board.port,
    #         fqbn=sel_board.fqbn,
    #         sketch_path=da_path.as_posix()
    #     )
    #     pprint(out)
    # except pyduinocli.errors.arduinoerror.ArduinoError as e:
    #     print("Error during compilation/upload/verification:")
    #     d = ast.literal_eval(str(e))
    #     pprint(d['__stderr'])
    #     return
    

if __name__ == "__main__":
    print(sys.argv)
    main()

