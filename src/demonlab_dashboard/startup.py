# startup.py
import asyncio

from textual.containers import Horizontal, Vertical
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
        yield Vertical(
            FigletWidget("Demonlab Dashboard", id="figlet1", font="small"),
            self.message,
            id="splash-stack",
        )

    async def on_mount(self):
        pass
