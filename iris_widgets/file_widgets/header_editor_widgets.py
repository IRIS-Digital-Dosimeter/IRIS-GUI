from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Button, Input, Collapsible, Label, Placeholder
from textual.message import Message
from textual.reactive import reactive
from textual import on, work
from textual_fspicker import FileOpen, Filters
from pathlib import Path

import iris_widgets.file_widgets.file_selection_widgets as fsw
import config_h_editor as che
import arduino_helper as ah

class HeaderEditorPanel(VerticalScroll):
    """Panel for editing a header file using the IRIS-Project's ."""
    
    config_handler: reactive[che.SketchConfigHandler | None] = reactive(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        # maps Input widget IDs to TOML entries
        self.input_mapping = {}
        
    
    
    # def compose(self) -> ComposeResult:
    #     with VerticalScroll(classes="panel"):
    #         yield Placeholder()
            
    def activate(self, sketch: ah.SketchStruct):
        
        header_path = sketch.path.parent / "config.h"
        self.config_handler = che.SketchConfigHandler(header_path)
        
        d = self.config_handler.retrieve()
        
        scrol = VerticalScroll()
        self.mount(scrol)
        for group_name, group in d.items():
            kids = []
            for k, v in group.items():
                label = Label(k, classes="config-option-label")
                input_field = Input(value=str(v), id=str(k), classes="config-option-input")
                h = Horizontal(label, Horizontal(classes="separator"), input_field, classes="config-option-horizontals")
                kids.append(h)

            scrol.mount(Collapsible(*kids, title=group_name, collapsed=False))
        