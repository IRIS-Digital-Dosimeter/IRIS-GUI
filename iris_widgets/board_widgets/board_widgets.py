from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, RadioSet, RadioButton, Button, Label, Input
from textual.message import Message
from textual.reactive import reactive
from textual.color import Color
from textual import on


from pathlib import Path

import arduino_helper as ah


class SelectedBoardDetails(Label):
    """Panel to display details of the selected board."""

    def show_board(self, board):
        self.update(str(board))
        self.styles.background = Color(0, 0, 0, a=0)
        
    def reset_state(self):
        if self.app.boards == []:
            self.update("No boards detected...")
            self.styles.background = "red 20%"
        else:
            self.update("No board selected...")
            self.styles.background = Color(0, 0, 0, a=0)
        
    def on_mount(self):
        self.reset_state()

class AutoBoardInfoPanel(Vertical):
    """Board list with a title on top, then radios + details side by side."""
    
    CSS_PATH = [
        Path(__file__).parent / "AutoBoardInfoPanel.tcss",
        Path(__file__).parent.parent / "base_classes.tcss"
    ]

    def compose(self) -> ComposeResult:
        with Vertical(classes="panel"):
            with Horizontal():
                with RadioSet(id="auto_board_list"):
                    for board in self.app.boards:
                        yield RadioButton(board.name)
                yield SelectedBoardDetails(id="board_details")
            yield Button("Refresh", id="refresh_boards_button")
        
    @on(RadioSet.Changed, "#auto_board_list")
    def post_option_changed(self, event: RadioSet.Changed):
        selected_index = [rb.value for rb in event.radio_set.children].index(True)
        board = self.app.boards[selected_index]
        details = self.query_one("#board_details", SelectedBoardDetails)
        details.show_board(board)

        event.stop()
        self.post_message(BoardChanged(board, is_manual=False))

    @on(Button.Pressed, "#refresh_boards_button")
    def post_refresh_board_list(self, event: Button.Pressed):
        self.post_message(RefreshAutoBoardList())
        
    def update_board_list(self, boards: list[ah.BoardStruct]):
        cur_board_list = self.query_one("#auto_board_list", RadioSet)
        cur_board_list.remove_children()
        new_boards = [RadioButton(board.name) for board in self.app.boards]
        cur_board_list.mount_all(new_boards)
        
        self.query_one("#board_details", SelectedBoardDetails).reset_state()
        
        

class BoardChanged(Message):
    def __init__(self, board: ah.BoardStruct | None, is_manual: bool):
        super().__init__()
        self.board = board
        self.is_manual = is_manual
        
class RefreshAutoBoardList(Message):
    def __init__(self):
        super().__init__()
        
        
######### Custom Board Selection Panel

class ManualBoardEntryPanel(Vertical):
    """Placeholder for manual board entry panel."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Input(placeholder="Board Name", id="manual_board_name")
            yield Input(placeholder="FQBN", id="manual_board_fqbn")
            yield Input(placeholder="Port", id="manual_board_port")
            yield Button("Select", id="manual_board_select_button")
            
    @on(Button.Pressed, "#manual_board_select_button")
    def apply_custom_board(self, event: Button.Pressed):
        name_input = self.query_one("#manual_board_name", Input)
        fqbn_input = self.query_one("#manual_board_fqbn", Input)
        port_input = self.query_one("#manual_board_port", Input)
        
        if not name_input.value or not fqbn_input.value or not port_input.value:
            self.app.notify("Please fill in all fields to select a custom board.", severity="error")
            return
        
        board = ah.BoardStruct(
            name=name_input.value,
            fqbn=fqbn_input.value,
            port=port_input.value,
            sn="N/A"
        )
        
        # event.stop()
        self.post_message(BoardChanged(board, is_manual=True))