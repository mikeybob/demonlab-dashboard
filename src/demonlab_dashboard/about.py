# about.py
import asyncio

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static
from textual_pyfiglet import FigletWidget

# TypeError: AboutScreen() compose() method returned an invalid result; 'NoneType' object is not iterable


class AboutScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Dismiss")]

    def compose(Screen) -> ComposeResult:
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
        # error occurs here: TypeError: AboutScreen() compose() method returned an invalid result; 'NoneType' object is not iterable
        Screen.about_text = Static(about_text, id="about-text")
        Screen.about_text.styles.color = "#FFFFFF"
        # Set the text color to white
        about_text = "[b]About DemonLab Dashboard[/b]"
        # error occurs here: TypeError: AboutScreen() compose() method returned an invalid result; 'NoneType' object is not iterable
        Screen.figlet_text = FigletWidget("Demonlab Dashboard", font="small")
        Screen.figlet_text.styles.color = "#FFFFFF"
        # Set the text color to white

    async def on_mount(Screen):
        yield Vertical(
            FigletWidget("Demonlab Dashboard", id="figlet-text", font="small"),
            Label(f"{about_text}", id="about-text"),
            id="about-box",
        )
