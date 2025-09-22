from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Static, RadioSet, RadioButton, Button, Label
from textual.message import Message
from textual.reactive import reactive
from textual import on, work
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
        
class SketchChanged(Message):
    def __init__(self, sketch: Path | None):
        super().__init__()
        self.sketch = sketch