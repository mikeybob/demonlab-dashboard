# clock.py
import asyncio
import datetime
from datetime import time

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Digits


class ClockWidget(Widget):
    """A simple digital clock using Digits widget."""

    time = reactive("")

    def compose(self) -> ComposeResult:
        yield Digits("", id="clock")

    async def on_mount(self):
        """Starts updating time once mounted."""
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.set_interval(1, self.update_time)

    def update_time(self):
        """Updates the time every second."""
        self.time = datetime.datetime.now().strftime("%H:%M:%S")

    def watch_time(self):
        """Called when the time attribute changes."""
        self.query_one(Digits).update(self.time)
