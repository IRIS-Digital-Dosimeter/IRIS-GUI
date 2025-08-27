from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, RadioSet, RadioButton
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

    @on(RadioSet.Changed, "#board_list")
    def option_changed(self, event: RadioSet.Changed):
        selected_index = [rb.value for rb in event.radio_set.children].index(True)
        board = self.app.boards[selected_index]
        details = self.query_one("#board_details", BoardDetails)
        details.show_board(board)
        
        print(Path(__file__).parent.as_posix())
        print(Path(__file__).parent.as_posix())
        print((Path(__file__).parent / "BoardInfoPanel.tcss").as_posix())

        event.stop()
        self.post_message(BoardChanged(board))


class BoardChanged(Message):
    def __init__(self, board: ah.BoardStruct | None):
        super().__init__()
        self.board = board