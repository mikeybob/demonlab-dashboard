# startup.py
import asyncio

from textual.screen import Screen
from textual.widgets import Static


class SplashScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Dismiss")]

    def compose(self):
        self.message = Static(
            "Welcome to the DemonLab Dashboard\nSystem Initializing...",
            id="splash-text",
        )
        self.message.styles.color = (
            "#000000"  # black/invisible text on black background initially
        )
        yield self.message

    async def on_mount(self):
        await self.fade_in_text()

    async def fade_in_text(self):
        # Fade-in steps from dark grey (#222222) to light (#ffffff)
        color_steps = ["#222222", "#555555", "#888888", "#BBBBBB", "#FFFFFF"]
        for shade in color_steps:
            self.message.styles.color = shade
            await asyncio.sleep(0.1)
