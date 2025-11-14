from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Static, RadioSet, RadioButton, Button, Label
from textual.message import Message
from textual.reactive import reactive
from textual import on, work
from textual.color import Color

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
            self.post_message(SketchChanged(opened))
            
            
            
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
        selected_sketch_path = list(self.app.preset_sketches.values())[selected_index]
        print(f"PRESET SKETCH: {selected_sketch_path}")
        self.post_message(SketchChanged(selected_sketch_path))
                        
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
    def __init__(self, sketch: Path | None):
        super().__init__()
        self.sketch = sketch