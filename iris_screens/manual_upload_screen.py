from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane
from textual.screen import Screen
from textual import on, work

from pathlib import Path

import iris_widgets.board_widgets.board_widgets as bw
import iris_widgets.file_widgets.file_selection_widgets as fsw
import iris_widgets.upload_widgets.upload_widgets as uw

class ManualUploadScreen(Screen):
    CSS_PATH = [
        Path(__file__).parent.parent / "iris_widgets" / "board_widgets" / "AutoBoardInfoPanel.tcss",
        Path(__file__).parent.parent / "iris_widgets" / "board_widgets" / "ManualBoardEntryPanel.tcss",
        Path(__file__).parent.parent / "iris_widgets" / "file_widgets" / "FileSelectionPanel.tcss",
        Path(__file__).parent.parent / "iris_widgets" / "upload_widgets" / "UploadSketchPanel.tcss",
    ]
    
    BINDINGS = [
        ("f", "pick_file", "Pick File"),
    ]
    
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        # with Vertical(id="main_container"):
        # yield bw.AutoBoardInfoPanel(id="board_selection_panel", classes="panel")
        yield Static(f"Board Selection", classes="title")
        with TabbedContent(classes="panel"):
            with TabPane("Detected Boards"):
                yield bw.AutoBoardInfoPanel(id="board_selection_panel")
            with TabPane("Manual Board Entry"):
                # yield Placeholder("Manual Board Entry Placeholder", id="manual_board_entry_panel")
                yield bw.ManualBoardEntryPanel(id="manual_board_entry_panel")
        
        yield Static("Sketch Selection", classes="title")
        yield fsw.FileSelectionPanel(id="file_selection_panel")

        yield Static("Upload Sketch Panel", classes="title")
        yield uw.UploadSketchPanel(id="upload_panel")


    @on(bw.BoardChanged)
    def on_board_changed(self, event: bw.BoardChanged) -> None:
        self.app.selected_board = event.board
        self.app.manual_board_entry = event.is_manual
        self.query_one("#upload_panel", uw.UploadSketchPanel).board_was_selected(event.board)


    @on(fsw.SketchChanged)
    def on_sketch_changed(self, event: fsw.SketchChanged) -> None:
        self.selected_sketch = event.sketch
        self.query_one("#upload_panel", uw.UploadSketchPanel).sketch_was_selected(event.sketch)


    @on(bw.BoardChanged)
    @on(fsw.SketchChanged)
    def update_upload_button(self) -> None:
        from time import sleep
        sleep(0.1)
        self.app.uploadable = (
            self.app.selected_board is not None and
            self.app.selected_sketch is not None and
            self.app.selected_sketch.exists()
        )
        # print(f"Uploadable: {self.app.uploadable}")
        # print(f"Selected Board: {self.app.selected_board}")
        # print(f"Selected Sketch: {self.app.selected_sketch}")
        # print(f"Sketch Exists: {self.app.selected_sketch.exists() if self.app.selected_sketch else 'N/A'}")

        upload_panel = self.query_one("#upload_panel", uw.UploadSketchPanel)
        upload_panel.query_one("#proceed_button").disabled = not self.app.uploadable
        
        
    @on(bw.RefreshAutoBoardList)
    @work(exclusive=True)
    async def refresh_board_list(self):
        self.app.boards = self.app.arduino.get_board_data() 
        self.query_one("#board_selection_panel", bw.AutoBoardInfoPanel).update_board_list(self.app.boards)
        

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
          