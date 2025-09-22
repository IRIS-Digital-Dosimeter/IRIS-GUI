from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, Markdown
from textual.screen import Screen

            
class IntroScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical():
            yield Static("Intro Screen Placeholder", classes="title")
            yield Markdown(INTRO_MD)

INTRO_MD = """\
# Welcome to the IRIS GUI!

## What is this?
This is a simple GUI application to help you upload Arduino sketches to your board.


"""