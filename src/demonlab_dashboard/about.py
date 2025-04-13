# about.py
import asyncio

from textual.screen import Screen
from textual.widgets import Static


class AboutScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Dismiss")]

    def compose(self):
        about_text = (
            "[b]DemonLab Dashboard[/b]\n"
            "Version: 0.0.1\n"
            "Author: Mike Demondad\n"
            "Contact: mike@demonlab.net\n"
            "License: MIT License\n\n"
            "This application provides an interactive interface\n"
            "for monitoring system health, alerts, and user activity\n"
            "on the DemonLab network."
        )
        self.message = Static(about_text, id="about-text")
        self.message.styles.color = "#000000"
        yield self.message

    async def on_mount(self):
        await self.fade_in_text()

    async def fade_in_text(self):
        color_steps = ["#222222", "#555555", "#888888", "#BBBBBB", "#FFFFFF"]
        for shade in color_steps:
            self.message.styles.color = shade
            await asyncio.sleep(0.1)
