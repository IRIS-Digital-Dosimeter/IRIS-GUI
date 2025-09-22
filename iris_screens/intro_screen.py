from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, Placeholder, OptionList, TabbedContent, TabPane, Markdown
from textual.screen import Screen, ModalScreen
from textual.reactive import reactive
from textual import on, work, events
from textual.binding import Binding
from textual.widgets.option_list import Option

from pathlib import Path

            
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