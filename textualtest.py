from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Static, RadioSet, RadioButton
from textual import on

import arduino_helper as ah


class BoardDetails(Static):
    """Panel to display details of the selected board."""

    def show_board(self, board):
        self.update(str(board))


class BoardList(Vertical):
    """Board list with a title on top, then radios + details side by side."""

    def __init__(self, boards: list[ah.BoardStruct], id=None):
        super().__init__(id=id)
        self.boards = boards

    def compose(self) -> ComposeResult:
        # Title at top
        yield Static("Available Boards", classes="boardlist-title")

        # Horizontal group containing RadioSet and BoardDetails
        with Horizontal():
            with RadioSet(id="board_list"):
                for board in self.boards:
                    yield RadioButton(board.name)
            yield BoardDetails(id="board_details")

    @on(RadioSet.Changed, "#board_list")
    def option_changed(self, event: RadioSet.Changed):
        selected_index = [rb.value for rb in event.radio_set.children].index(True)
        board = self.boards[selected_index]
        details = self.query_one("#board_details", BoardDetails)
        details.show_board(board)


class TestApp(App):
    CSS = """
    .boardlist-title {
        content-align: center middle;
        height: 3;
        text-style: bold;
        border: solid gray;
    }
    
    #board_list {
        width: 40%;
        min-width: 25;
        border: solid gray;
        height: 8;
    }

    #board_details {
        width: 60%;
        border: solid gray;
        padding: 1;
        height: 8;
    }
    
    #vert_of_board_list {
        border: solid gray
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode")
    ]

    def __init__(self, boards: list[ah.BoardStruct]):
        super().__init__()
        self.boards = boards

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield BoardList(boards=self.boards, id='#vert_of_board_list')

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    arduino = ah.ExtendoArduino(
        additional_urls=[
            'https://adafruit.github.io/arduino-board-index/package_adafruit_index.json'
        ],
    )

    boards = arduino.get_board_data()
    app = TestApp(boards=boards)
    app.run()
