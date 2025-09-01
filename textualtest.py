from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, Placeholder, OptionList
from textual.screen import Screen, ModalScreen
from textual.reactive import reactive
from textual import on, work, events
from textual.binding import Binding
from textual.widgets.option_list import Option

import iris_widgets.board_widgets.board_widgets as bw
import iris_widgets.file_widgets.file_selection_widgets as fsw
import iris_widgets.upload_widgets.upload_widgets as uw

from textual_fspicker import FileOpen, Filters
from pathlib import Path
from pprint import pprint

import arduino_helper as ah



class ManualUploadScreen(Screen):
    CSS_PATH = [
        Path(__file__).parent / "iris_widgets" / "board_widgets" / "BoardInfoPanel.tcss",
        Path(__file__).parent / "iris_widgets" / "file_widgets" / "FileSelectionPanel.tcss",
        Path(__file__).parent / "iris_widgets" / "upload_widgets" / "UploadSketchPanel.tcss",
    ]
    
    BINDINGS = [
        ("f", "pick_file", "Pick File"),
    ]
    
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical(id="main_container"):
            yield bw.BoardInfoPanel(id="board_selection_panel")
            yield fsw.FileSelectionPanel(id="file_selection_panel")
            yield uw.UploadSketchPanel(id="upload_panel")


    @on(bw.BoardChanged)
    def on_board_changed(self, event: bw.BoardChanged) -> None:
        self.app.selected_board = event.board
        self.query_one("#upload_panel", uw.UploadSketchPanel).board_was_selected(event.board)


    @on(fsw.SketchChanged)
    def on_sketch_changed(self, event: fsw.SketchChanged) -> None:
        self.selected_sketch = event.sketch
        self.query_one("#upload_panel", uw.UploadSketchPanel).sketch_was_selected(event.sketch)


    @on(bw.BoardChanged)
    @on(fsw.SketchChanged)
    def update_upload_button(self) -> None:
        self.app.uploadable = (
            self.app.selected_board is not None and
            self.app.selected_sketch is not None and
            self.app.selected_sketch.exists()
        )
        upload_panel = self.query_one("#upload_panel", uw.UploadSketchPanel)
        upload_panel.query_one("#proceed_button").disabled = not self.app.uploadable
        
        
    @on(bw.RefreshBoardList)
    @work(exclusive=True)
    async def refresh_board_list(self):
        self.app.boards = self.app.arduino.get_board_data() 
        self.query_one("#board_selection_panel", bw.BoardInfoPanel).update_board_list(self.app.boards)
        

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
        
        
    @work
    async def action_pick_file(self) -> None:
        """Show a filepicker screen."""
        
        if opened := await self.app.push_screen_wait(FileOpen(
            filters=Filters(
                ("Arduino Sketch", lambda f: f.suffix.lower() == ".ino")
            )
        )):
            self.query_one("#selected_file_label").update(str(opened))

            self.post_message(fsw.SketchChanged(opened))
            
            
class ScreenPicker(ModalScreen):
    CSS_PATH = [
        Path(__file__).parent / "iris_screens" / "screen_picker.tcss"
    ]
    
    
    def compose(self) -> ComposeResult:
        self.screens_as_options = {}
        
        for i, (k,v) in enumerate(self.app.SCREENS.items()):
            opt_name = f"{i+1}. {v.__name__}"

            o = Option(opt_name, id=k)
            self.screens_as_options[f"{i+1}"] = o
            
        out = []
        for o in self.screens_as_options.values():
            out.append(o)
            out.append(None)
        out.pop()
        

        yield OptionList(*out)
        
        
    @on(OptionList.OptionSelected)
    def screen_picked(self, event: OptionList.OptionSelected):
        self.app.switch_screen(event.option.id)
        
    
    @on(events.Key)
    def change_screen_on_num(self, event: events.Key):
        if event.key.isdecimal() and event.key in self.screens_as_options.keys():
            self.app.switch_screen(self.screens_as_options[event.key].id)
        
        
            
class IntroScreen(Screen):
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical():
            yield Static("Intro Screen Placeholder", classes="title")
            yield Placeholder("test pacehlder")
            
    
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
