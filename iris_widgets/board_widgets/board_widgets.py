from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, RadioSet, RadioButton, Button
from textual.message import Message
from textual.reactive import reactive
from textual import on

from pathlib import Path

import arduino_helper as ah


class BoardDetails(Static):
    """Panel to display details of the selected board."""

    def show_board(self, board):
        self.update(str(board))


class BoardInfoPanel(Vertical):
    """Board list with a title on top, then radios + details side by side."""
    
    CSS_PATH = [
        Path(__file__).parent / "BoardInfoPanel.tcss",
        Path(__file__).parent.parent / "base_classes.tcss"
    ]

    selected_board: reactive[ah.BoardStruct | None] = reactive(None)
    
    def compose(self) -> ComposeResult:
        # Title at top
        yield Static(f"Board Information", classes="title")

        # Horizontal group containing RadioSet and BoardDetails
        with Horizontal():
            with RadioSet(id="board_list"):
                for board in self.app.boards:
                    yield RadioButton(board.name)
            yield BoardDetails(id="board_details")
        yield Button("Refresh", id="refresh_boards_button")

    @on(RadioSet.Changed, "#board_list")
    def post_option_changed(self, event: RadioSet.Changed):
        selected_index = [rb.value for rb in event.radio_set.children].index(True)
        board = self.app.boards[selected_index]
        details = self.query_one("#board_details", BoardDetails)
        details.show_board(board)
        

        event.stop()
        self.post_message(BoardChanged(board))

    @on(Button.Pressed, "#refresh_boards_button")
    def post_refresh_board_list(self, event: Button.Pressed):
        self.post_message(RefreshBoardList())
        
        
    def refresh_board_list(self, boards: list[ah.BoardStruct]):
        cur_board_list = self.query_one("#board_list", RadioSet)
        cur_board_list.remove_children()
        new_boards = [RadioButton(board.name) for board in self.app.boards]
        cur_board_list.mount_all(new_boards)
        

class BoardChanged(Message):
    def __init__(self, board: ah.BoardStruct | None):
        super().__init__()
        self.board = board
        
class RefreshBoardList(Message):
    def __init__(self):
        super().__init__()