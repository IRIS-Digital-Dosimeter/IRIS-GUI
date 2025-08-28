from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Static, RadioSet, RadioButton, Button, Label
from textual.message import Message
from textual.reactive import reactive
from textual import on, work, events

import iris_widgets.board_widgets.board_widgets as bw
import iris_widgets.file_widgets.file_selection_widgets as fsw
import iris_widgets.upload_widgets.upload_widgets as uw

from textual_fspicker import FileOpen, Filters
from pathlib import Path

import arduino_helper as ah



        
        
class TestApp(App):
    CSS_PATH = [
        Path(__file__).parent / "iris_widgets" / "base_classes.tcss",
        Path(__file__).parent / "iris_widgets" / "board_widgets" / "BoardInfoPanel.tcss",
        Path(__file__).parent / "iris_widgets" / "file_widgets" / "FileSelectionPanel.tcss",
        Path(__file__).parent / "iris_widgets" / "upload_widgets" / "UploadSketchPanel.tcss",
    ]

    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"),
        ("f", "pick_file", "Pick File"),
        ("ctrl+q", "quit", "Quit"),
    ]
    
    selected_sketch: reactive[str | None] = reactive(None)
    selected_board: reactive[ah.BoardStruct | None] = reactive(None)

    def __init__(self, arduino: ah.ExtendoArduino):
        super().__init__()
        self.arduino = arduino
        self.boards = arduino.get_board_data()
        self.uploadable = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical(id="main_container"):
            yield bw.BoardInfoPanel(id="board_selection_panel")
            yield fsw.FileSelectionPanel(id="file_selection_panel")
            yield uw.UploadSketchPanel(id="upload_panel")

    @on(bw.BoardChanged)
    def on_board_changed(self, event: bw.BoardChanged) -> None:
        self.selected_board = event.board
        self.query_one("#upload_panel", uw.UploadSketchPanel).board_was_selected(event.board)

    @on(fsw.SketchChanged)
    def on_sketch_changed(self, event: fsw.SketchChanged) -> None:
        self.selected_sketch = event.sketch
        self.query_one("#upload_panel", uw.UploadSketchPanel).sketch_was_selected(event.sketch)

    @on(bw.BoardChanged)
    @on(fsw.SketchChanged)
    def update_upload_button(self) -> None:
        self.uploadable = (
            self.selected_board is not None and
            self.selected_sketch is not None and
            self.selected_sketch.exists()
        )
        upload_panel = self.query_one("#upload_panel", uw.UploadSketchPanel)
        upload_panel.query_one("#proceed_button").disabled = not self.uploadable
        
    @on(bw.RefreshBoardList)
    def refresh_board_list(self):
        self.boards = self.arduino.get_board_data() 
        
        self.query_one("#board_selection_panel", bw.BoardInfoPanel).refresh_board_list(self.boards)
        
        

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


if __name__ == "__main__":
    arduino = ah.ExtendoArduino(
        additional_urls=[
            'https://adafruit.github.io/arduino-board-index/package_adafruit_index.json'
        ],
    )

    app = TestApp(arduino=arduino)
    app.run()
