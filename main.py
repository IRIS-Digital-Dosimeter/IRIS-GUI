import pyduinocli
from pprint import pprint

def main():
    print("Hello from iris-gui!")   
    cli = pyduinocli.Arduino(additional_urls=['https://adafruit.github.io/arduino-board-index/package_adafruit_index.json'])
    print(type(cli))
    # pprint(cli.version()['result'])
    
    pprint(cli.board.list()['result']['detected_ports'][0])


if __name__ == "__main__":
    main()

