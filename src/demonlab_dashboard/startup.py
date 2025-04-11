from textual.screen import Screen
from textual.widgets import Static
import asyncio

class SplashScreen(Screen):
    def compose(self):
        yield Static(
            "Welcome to the DemonLab Dashboard\\nSystem Initializing...",
            id="splash-text"
        )

    async def on_mount(self):
        await self.animate_fade_in()

    async def animate_fade_in(self):
        self.set_opacity(0)
        while self.get_opacity() &lt; 1:
            self.set_opacity(self.get_opacity() + 0.05)
            await asyncio.sleep(0.05)
