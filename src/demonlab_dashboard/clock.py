# clock.py
import asyncio
import datetime

from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Digits


class ClockWidget(Widget):
    """A simple digital clock using Digits widget."""

    time = reactive("00:00:00")  # Reactive state to store time

    async def on_mount(self):
        """Starts updating time once mounted."""
        self.digits = Digits(self.time)
        self.update(self.digits)
        asyncio.create_task(self.update_time())

    async def update_time(self):
        """Updates the time every second."""
        while True:
            self.time = datetime.datetime.now().strftime("%H:%M:%S")
            await asyncio.sleep(1)

    def render(self):
        """Updates the displayed time."""
        self.digits.update(self.time)
        return self.digits
