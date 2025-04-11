from textual.screen import Screen
from textual.widgets import Static
import asyncio

class AboutScreen(Screen):
    def compose(self):
        yield Static(
            "[b]DemonLab Dashboard[/b]\\n"
            "Version: 0.0.1\\n"
            "Author: Mike Demondad\\n"
            "Contact: mike@demonlab.net\\n"
            "License: MIT License\\n"
            "\\n"
            "This application provides an interactive interface for monitoring\\n"
            "system health, alerts, and user activity on the DemonLab network.",
            id="about-text"
        )

    async def on_mount(self):
        await self.animate_fade_in()

    async def animate_fade_in(self):
        self.set_opacity(0)
        while self.get_opacity() &lt; 1:
            self.set_opacity(self.get_opacity() + 0.05)
            await asyncio.sleep(0.05)
