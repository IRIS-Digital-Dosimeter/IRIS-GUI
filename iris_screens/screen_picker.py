from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, Placeholder, OptionList, TabbedContent, TabPane, Markdown
from textual.screen import Screen, ModalScreen
from textual.reactive import reactive
from textual import on, work, events
from textual.binding import Binding
from textual.widgets.option_list import Option

from pathlib import Path

import iris_widgets.board_widgets.board_widgets as bw
import iris_widgets.file_widgets.file_selection_widgets as fsw
import iris_widgets.upload_widgets.upload_widgets as uw


class ScreenPicker(ModalScreen):
    CSS_PATH = [
        Path(__file__).parent / "screen_picker.tcss"
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
        