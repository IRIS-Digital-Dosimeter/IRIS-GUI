from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, Placeholder, OptionList, TabbedContent, TabPane, Markdown
from textual.screen import Screen, ModalScreen
from textual.reactive import reactive
from textual import on, work, events
from textual.binding import Binding
from textual.widgets.option_list import Option

import iris_widgets.board_widgets.board_widgets as bw
import iris_widgets.file_widgets.file_selection_widgets as fsw
import iris_widgets.upload_widgets.upload_widgets as uw

from iris_screens.screen_picker import ScreenPicker
from iris_screens.manual_upload_screen import ManualUploadScreen
from iris_screens.intro_screen import IntroScreen


from textual_fspicker import FileOpen, Filters
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
    }
    
    selected_sketch: reactive[str | None] = reactive(None)
    selected_board: reactive[ah.BoardStruct | None] = reactive(None)
    boards: reactive[list[ah.BoardStruct]] = reactive([])

    def __init__(self, arduino: ah.ExtendoArduino):
        super().__init__()
        self.arduino = arduino
        self.boards = arduino.get_board_data()
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

    app = IrisApp(arduino=arduino)
    app.run()
