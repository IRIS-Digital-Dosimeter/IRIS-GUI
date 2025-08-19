import pyduinocli
import arduino_helper as a_h
import ast
import crossfiledialog
from pathlib import Path
from pprint import pprint

def main():
    # install the arduino-cli, board reqs, and lib reqs if not installed
    ardu = a_h.ExtendoArduino(additional_urls=['https://adafruit.github.io/arduino-board-index/package_adafruit_index.json'])
    out = ardu.install_cores()
    print('M0 reqs installed')
    
    
    # pprint(ardu.lib.list())
    out = ardu.install_default_libs()
    print('Default libs installed')
    

    boards = ardu.get_board_data()
    print('found boards:')
    for n, board_deets in enumerate(boards):
        print('---------------------------------')
        print(f"{n}:")
        print(board_deets)
        print('---------------------------------')
        print()

    # pick the right board manually :
    board_num = int(input('Enter the number of the board to use: '))
    sel_board = boards[board_num]
    # port, FQBN, core = boards[board_num]
    
    print("Selected Board:")
    print('---------------------------------')
    print(sel_board)
    print('---------------------------------')
    

    # da_path = "/home/paelen/Documents/GitHub/IRIS-Project/packages/M0/Binary Serial Logger/serial_log/serial_log.ino"
    # da_path = "C:\\Users\\Sevak\\Documents\\GitHub\\IRIS-Project\\packages\\M0\\Binary Serial Logger\\serial_log\\serial_log.ino"

    da_path = Path(crossfiledialog.open_file(title="Select an Arduino sketch (.ino) file", filter="*.ino")).resolve()
    # da_path = Path("C:\\Users\\Sevak\\Documents\\GitHub\\IRIS-Project\\packages\\M0\\Binary Serial Logger\\serial_log\\serial_log.ino").resolve()
    
    print(f"DA PATH: {da_path}")

    # # compile_upload_verify(port, FQBN, '"C:\\Users\\SEVAK\\Documents\\GitHub\\IRIS-Project\\sandbox\\M0\\mass storage andrew\\msc_sdfat\\msc_sdfat.ino"', usbstack='tinyusb')
    # # compile_upload_verify(port, FQBN, '"/home/paelen/Documents/GitHub/IRIS-Project/sandbox/M0/SdFat/datalogger_tAv_bin/datalogger_tAv_bin.ino"', usbstack='tinyusb')
    # # compile_upload_verify(port, FQBN, '"/home/paelen/paelen.ino"')
    try:
        out = ardu.compile_upload_verify(
            port=sel_board.port,
            fqbn=sel_board.fqbn,
            sketch_path=da_path.as_posix()
        )
        pprint(out)
    except pyduinocli.errors.arduinoerror.ArduinoError as e:
        print("Error during compilation/upload/verification:")
        d = ast.literal_eval(str(e))
        pprint(d['__stderr'])
        return
    

if __name__ == "__main__":
    main()

