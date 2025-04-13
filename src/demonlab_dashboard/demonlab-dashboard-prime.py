# demonlab-dashboard-prime.py
from about import AboutScreen
from startup import SplashScreen
from textual.app import App
from textual.binding import Binding
from textual.widgets import Footer, Header


class GridLayoutTest(App):
    CSS_PATH = "demonlab-dashboard.tcss"
    TITLE = "Admin Dashboard"
    SUB_TITLE = "Demonlab"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="push_screen('about')",
            description="Show about screen",
            key_display="?",
        ),
        Binding(
            key="s",
            action="push_screen('splash')",
            description="Show startup screen",
            key_display="s",
        ),
    ]

    async def on_mount(self):
        # Show splash screen initially
        await self.push_screen(SplashScreen())
        self.set_timer(
            3, self.switch_to_about
        )  # Automatically switch to about screen after 3 seconds

    def switch_to_about(self):
        # Transition to the AboutScreen after splash
        self.push_screen(AboutScreen())

    def compose(self):
        yield Footer()
        yield Header()
        # Add other main screen components here


if __name__ == "__main__":
    app = GridLayoutTest()
    app.run()
