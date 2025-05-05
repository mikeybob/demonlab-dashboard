from textual.app import App, ComposeResult
from textual.widgets import Button, Static

from database import Database
from system_health import SystemHealthPanel

# Import other necessary modules


class MainApp(App):
    def compose(self) -> ComposeResult:
        # Include components from other modules
        yield SystemHealthPanel()
        # Add more panels or widgets as needed
        yield Static("[b]Options Misc2[/b]", classes="box", id="opts")

    async def on_mount(self):
        # Mount tasks or panels
        await Database.connect()
        # Schedule periodic tasks if necessary


if __name__ == "__main__":
    app = MainApp()
    app.run()
