from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button, Label
from textual.message import Message
from textual.reactive import reactive
from textual import on, work

from pathlib import Path

import arduino_helper as ah


class UploadSketchPanel(Vertical):
    CSS_PATH = [
        Path(__file__).parent / "UploadSketchPanel.tcss",
        Path(__file__).parent.parent / "base_classes.tcss"
    ]
    
    
    def compose(self) -> ComposeResult:
        with Vertical(classes="panel"):
            with Horizontal():
                yield StatusIndicator(valid = False, text = "Board", subtext="Not Selected", id="board_status", classes="status-label status-invalid")
                yield StatusIndicator(valid = False, text = "Sketch", subtext="Not Selected", id="sketch_status", classes="status-label status-invalid")
            yield Button("Proceed", id="proceed_button", disabled=True)
    
    @on(Button.Pressed, "#proceed_button")
    def upload_sketch_process(self, event: Button.Pressed):
        """Handle the upload button press."""
        
        if self.app.manual_board_entry == False:
            if self.verify_selected_board() == False:
                print("board failed!")
                self.app.notify("Please select a valid board.", severity="error")
                self.board_was_selected(None)
                self.app.query_one("#board_selection_panel").focus()
                return
        if self.verify_selected_sketch() == False:
            print("sketch failed!")
            self.app.notify("Please select a valid sketch", severity="error")
            self.sketch_was_selected(None)
            self.app.query_one("#file_selection_panel").focus()
            return
            
        if not self.app.uploadable:
            self.app.notify("Please select a valid board and sketch before proceeding.", severity="error")
            return
        
        sketch = self.app.selected_sketch
        board = self.app.selected_board
        
        print(f"Uploading sketch {sketch} to board {board.fqbn} on port {board.port}")
        
        if sketch and board:
            try:
                result = self.app.arduino.compile_upload_verify(
                    port=board.port,
                    fqbn=board.fqbn,
                    sketch_path=sketch.as_posix()
                )
                self.app.notify(f"Upload successful: [placeholder]", severity="success")
            except Exception as e:
                self.app.notify(f"Upload failed: [placeholder]", severity="error")
        else:
            self.app.notify("Invalid board or sketch selected.", severity="error")
        
    def verify_selected_board(self) -> bool:
        self.app.screen.refresh_board_list()
        return self.app.selected_board in self.app.boards
        
    def verify_selected_sketch(self) -> bool:
        return Path(self.app.selected_sketch).is_file()
        
        
    def sketch_was_selected(self, sketch: Path | None) -> None:
        self.app.selected_sketch = sketch
        sketch_label = self.query_one("#sketch_status", StatusIndicator)
        if sketch:
            sketch_label.set_validity(True)
            sketch_label.set_text("Sketch", sketch.name)
        else:
            sketch_label.set_validity(False)
            sketch_label.set_text("Sketch", "Not Selected")
        self.refresh()
        
    def board_was_selected(self, board: ah.BoardStruct | None) -> None:
        board_status = self.query_one("#board_status", StatusIndicator)
        if board:
            board_status.set_validity(True)
            board_status.set_text("Board", board.fqbn)
        else:
            board_status.set_validity(False)
            board_status.set_text("Board", "Not Selected")
        self.refresh()
        
class StatusIndicator(Label):
    """A Static that indicates the status of a selection."""

    r_text: reactive[str | None] = reactive(None, recompose=True)
    r_subtext: reactive[str | None] = reactive(None, recompose=True)
    r_valid: reactive[bool] = reactive(False, recompose=True)
    
    def __init__(self, valid: bool, text: str, subtext:str = "", **kwargs):
        r_text = text
        r_subtext = subtext
        r_valid = valid
        
        super().__init__("", **kwargs)
        self.set_text(r_text, r_subtext)
        
    def compose(self) -> ComposeResult:
        yield Label(self.r_text)
    
    def set_validity(self, valid: bool) -> None:
        """Update the validity of the status."""
        self.r_valid = valid
        self.mutate_reactive(StatusIndicator.r_valid)
        self.set_text(self.r_text, self.r_subtext)
        
        if valid:
            self.remove_class("status-invalid")
            self.add_class("status-valid")
        else:
            self.remove_class("status-valid")
            self.add_class("status-invalid")
        
        
    def set_text(self, text: str, subtext: str = "") -> None:
        """Update the text of the status."""
        checked = "✅" if self.r_valid else "❌"
        self.r_text = f"{checked} {text}"
        if subtext != "":
            self.r_text += f": {subtext}"
        self.update(self.r_text)
        self.mutate_reactive(StatusIndicator.r_text)