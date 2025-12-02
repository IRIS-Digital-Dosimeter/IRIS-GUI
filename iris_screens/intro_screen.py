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
# Screens
The GUI is split into several "screens". You can switch between them with **CTRL+S**. You're also prompted at startup to choose a screen.
## ManualUploadScreen
Allows you to manually select a sketch to upload, and view the associated `config.h` file if the sketch supports a standard one. Note that the "config editor" tab is read-only. 
## MDAScreen
Preset sketches are included in the **MDAScreen**:
- **Binary Serial Logger**
	- Constantly dumps samples over the serial line.
	- Can use the included **serial_importer_all_in_one** script to read the data.
- **M4 Datalogger**
	- Logs data continuously on 4 pins at high speeds to the SD card.
- **Toggle Switch Datalogger**
	- Uses a physical switch to enable/disable data logging on 4 pins at high speeds to the SD card.
- **SD Card Exposer**
	- Exposes the onboard SD card as a flash drive to the connected computer. Poor performance.


"""