from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Static, RadioSet, RadioButton, Button, Label, OptionList
from textual.message import Message
from textual.reactive import reactive
from textual import on, work
from textual.color import Color
import arduino_helper as ah

from textual_fspicker import FileOpen, Filters


from pathlib import Path


class FileSelectionPanel(Vertical):
    """Panel for selecting a sketch file."""
    
    
    def compose(self) -> ComposeResult:
        with Vertical(classes="panel"):
            yield Label("Select a sketch file:", classes="file-label")
            with Horizontal(id="browse_row"):
                yield Button("Browse", id="browse_button")
                yield Label("No file selected", id="selected-file-label")

    def get_selected_usb_stack(self) -> ah.USBStack:
        highlighted_usbstack_index = self.app.screen.query_one("#usb_stack_option_list").highlighted
        highlighted_usbstack = ah.USBStack.list()[highlighted_usbstack_index]
        return highlighted_usbstack
    
    @on(Button.Pressed, "#browse_button")
    @work
    async def action_pick_file(self, event:Button.Pressed) -> None:
        """Show a filepicker screen."""
        
        if opened := await self.app.push_screen_wait(FileOpen(
            filters=Filters(
                ("Arduino Sketch", lambda f: f.suffix.lower() == ".ino")
            )
        )):
            self.query_one("#selected-file-label").update(str(opened))

            event.stop()
            cur_usbstack = self.get_selected_usb_stack()
            new_sketch_struct = ah.SketchStruct(opened, cur_usbstack)
            self.post_message(SketchChanged(new_sketch_struct))
            
    @on(OptionList.OptionSelected)
    def action_select_usbstack(self, event:OptionList.OptionSelected) -> None:
        highlighted_usbstack = self.get_selected_usb_stack()
        if self.app.selected_sketch:
            cur_sketch_path = self.app.selected_sketch.path
            new_sketch_struct = ah.SketchStruct(cur_sketch_path, highlighted_usbstack)
            self.post_message(SketchChanged(new_sketch_struct))
            
            
            
class PresetFileSelectionPanel(Vertical):
    """Panel for selecting a sketch from several preset sketches."""
    
    def compose(self) -> ComposeResult:
        with Vertical(classes="panel"):
            with Horizontal():
                with RadioSet(id="preset_sketch_list"):
                    # sketch should be a Path from pathlib
                    for k in self.app.preset_sketches.keys():
                        yield RadioButton(k)
                yield SelectedSketchDetails(id="sketch_details")

    @on(RadioSet.Changed, "#preset_sketch_list")
    def post_sketch_changed(self, event: RadioSet.Changed):
        event.stop()
        
        selected_index = [rb.value for rb in event.radio_set.children].index(True)
        selected_sketch = list(self.app.preset_sketches.values())[selected_index]
        self.post_message(SketchChanged(selected_sketch))
                        
class SelectedSketchDetails(Label):
    """Panel to display details of the selected sketch."""

    def show_sketch(self, sketch: Path):
        self.update(sketch.as_posix)
        
    def reset_state(self):
        if self.app.preset_sketches == {}:
            self.update("No preset sketches...")
        else:
            self.update("No Sketch selected...")
        
    def on_mount(self):
        self.reset_state()            
            
        
class SketchChanged(Message):
    def __init__(self, sketch: ah.SketchStruct | None):
        super().__init__()
        self.sketch = sketch