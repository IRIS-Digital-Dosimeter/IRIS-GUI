import pyduinocli
import arduino_helper as a_h
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
    

    da_path = "/home/paelen/Documents/GitHub/IRIS-Project/packages/M0/Binary Serial Logger/serial_log/serial_log.ino"
    
    # import tkinter as tk
    # from tkinter import filedialog
    # root = tk.Tk()
    # root.withdraw()
    # da_path = filedialog.askopenfilename()

    # # compile_upload_verify(port, FQBN, '"C:\\Users\\SEVAK\\Documents\\GitHub\\IRIS-Project\\sandbox\\M0\\mass storage andrew\\msc_sdfat\\msc_sdfat.ino"', usbstack='tinyusb')
    # # compile_upload_verify(port, FQBN, '"/home/paelen/Documents/GitHub/IRIS-Project/sandbox/M0/SdFat/datalogger_tAv_bin/datalogger_tAv_bin.ino"', usbstack='tinyusb')
    # # compile_upload_verify(port, FQBN, '"/home/paelen/paelen.ino"')
    out = ardu.compile_upload_verify(
        port=sel_board.port,
        fqbn=sel_board.fqbn,
        sketch_path=da_path
    )
    
    pprint(out)
    

if __name__ == "__main__":
    main()

