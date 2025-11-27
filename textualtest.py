from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.binding import Binding

from iris_screens.screen_picker import ScreenPicker
from iris_screens.manual_upload_screen import ManualUploadScreen
from iris_screens.intro_screen import IntroScreen
from iris_screens.mda_screen import MDAScreen


from pathlib import Path
from pprint import pprint

import arduino_helper as ah
            
    
class IrisApp(App):
    CSS_PATH = [
        Path(__file__).parent / "iris_widgets" / "base_classes.tcss",
    ]

    BINDINGS = [
        Binding(key="ctrl+s", action="switch", description="Switch Screens", priority=True),
        Binding(key="d", action="toggle_dark", description="Toggle Dark Mode", priority=True),
        Binding(key="ctrl+q", action="quit", description="Quit", priority=True),
    ]
    
    SCREENS = {
        "man_screen": ManualUploadScreen,
        "intro_screen": IntroScreen,
        "mda_screen": MDAScreen,
    }
    
    selected_sketch: reactive[ah.SketchStruct | None] = reactive(None)
    selected_board: reactive[ah.BoardStruct | None] = reactive(None)
    boards: reactive[list[ah.BoardStruct]] = reactive([])

    def __init__(self, arduino: ah.ExtendoArduino, preset_sketches: dict[str, ah.SketchStruct]):
        super().__init__()
        self.arduino = arduino
        self.boards = arduino.get_board_data()
        self.preset_sketches = preset_sketches
        
        self.uploadable = False
        self.manual_board_entry = False
        
        
    def on_mount(self):
        self.push_screen(ScreenPicker())
        

    def action_switch(self):
        self.push_screen(ScreenPicker())



if __name__ == "__main__":
    arduino = ah.ExtendoArduino(
        additional_urls=[
            'https://adafruit.github.io/arduino-board-index/package_adafruit_index.json'
        ],
    )
    
    preset_sketch_folder = Path(__file__).parent / "preset_sketches"
    preset_sketches = {
        "Binary Serial Logger": ah.SketchStruct(preset_sketch_folder / "Binary Serial Logger" / "serial_log" / "serial_log.ino", ah.USBStack.ARDUINO_STACK),
        "M4 Datalogger": ah.SketchStruct(preset_sketch_folder / "M4 Datalogger" / "dma_dual_adc_unified_SdFat" / "dma_dual_adc_unified_SdFat.ino", ah.USBStack.ARDUINO_STACK),
        "SD Card Exposer": ah.SketchStruct(preset_sketch_folder / "SD Card Exposer" / "msc_sdfat" / "msc_sdfat.ino", ah.USBStack.TINYUSB_STACK),
        "Toggle Switch Datalogger": ah.SketchStruct(preset_sketch_folder / "Toggle Switch Datalogger" / "dma_dual_adc_unified_SdFat" / "dma_dual_adc_unified_SdFat.ino", ah.USBStack.ARDUINO_STACK),
    }
    files_exist = all(sketch.path.exists() for sketch in preset_sketches.values())
    if files_exist:
        print("All preset sketches exist!")
    else:
        print("Check preset sketches...")
        exit()
    
    

    app = IrisApp(arduino=arduino, preset_sketches=preset_sketches)
    app.run()
