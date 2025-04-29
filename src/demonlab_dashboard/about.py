# about.py
import asyncio

from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static
from textual_pyfiglet import FigletWidget


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
        self.message.styles.color = "#FFFFFF"
        yield Vertical(
            FigletWidget("Demonlab Dashboard", id="abtfiglet", font="small"),
            Static(about_text, id="abttext"),
            id="abtfigbox",
        )

    async def on_mount(self):

        yield Vertical(
            FigletWidget("2 Demonlab Dashboard", id="abtfiglet", font="small"),
            Static(f"{about_text}", id="abttext"),
        )
