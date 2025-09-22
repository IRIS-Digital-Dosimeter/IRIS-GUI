from textual.app import App, ComposeResult
from textual.widgets import OptionList
from textual.screen import ModalScreen
from textual import on, events
from textual.widgets.option_list import Option

from pathlib import Path


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
        