# startup.py
import asyncio

from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Static
from textual_pyfiglet import FigletWidget


class SplashScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Dismiss")]

    def compose(self):
        self.message = Static(
            "Welcome to the DemonLab Dashboard\nSystem Initializing...",
            id="splash-text",
        )
        self.message.styles.color = "white"
        yield self.message

    async def on_mount(self):
        # yield self.message
        yield Horizontal(FigletWidget("Label of Things", id="figlet1", font="small"))

    #     push_screen(SplashScreen())
    #     await asyncio.sleep(0.1)
