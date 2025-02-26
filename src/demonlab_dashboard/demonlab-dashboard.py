from clock import ClockWidget  # Import the clock widget
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, HorizontalScroll, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Digits,
    Footer,
    Header,
    Label,
    LoadingIndicator,
    Placeholder,
    Static,
)

# UserPanel Glyphs
tz = "[red] GMT[/red]"
login_gap = "[darkorange] 1d 2h 3m[/darkorange]"
status = "[green] Active[/green]"
status_msg = "[seagreen]My status message is Hi![/seagreen]"
# GlyphBar Glyphs
cog = "[blue bold][/blue bold]"
bolt = "[crimson bold][/crimson bold]"
fluffychat = "[purple bold] [/purple bold]"
element = "[purple][/purple]"
cinny = "[aqua bold][/aqua bold]"
turtle = "[limegreen bold]T[/limegreen bold]"
checkflag = "[white bold][/white bold]"
globe = "[dodgerblue bold][/dodgerblue bold]"
lock = "[orange bold][/orange bold]"
star = "[darkred bold][/darkred bold]"
person = "[#FFC300][/#FFC300]"
ghost = "[#FFC300][/#FFC300]"


class SplashScreen(Screen):
    pass


class Settings(Screen):
    pass


class Anomoly(Screen):
    pass


class Alerts(Screen):
    pass


class Misc(Screen):
    pass


class SystemHealth(Screen):
    pass


class GridLayoutTest(App):
    CSS_PATH = "demonlab-dashboard.tcss"

    TITLE = "Admin Dashboard"
    SUB_TITLE = "Demonlab"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="b", action="null", description="Beep"),
        Binding(key="p", action="null2", description="Plop"),
    ]

    #  async def compose(self) -> ComposeResult:
    def compose(self) -> ComposeResult:
        """Composes the UI layout with a clock."""
        yield Footer()
        yield Header()
        #  yield ClockWidget()  # Add clock widget
        #  yield self.create_button_panel()

        for user_no in range(1, 13):
            glyphs = f"{lock} {ghost} {globe} {bolt} {cog} {cinny} {star} {element} {turtle} {checkflag} {person} {fluffychat}"
            Content = f"[yellow]@User{user_no}:demonlab.net[/yellow]\n\n{tz} {login_gap}   {status}\n{status_msg}\n\n\n   {glyphs}"
            yield Label(Content, id=f"User{user_no}", classes="box")
            self.border_title = f"UserName{user_no}"
            self.border_subtitle = f"DisplayName"

        yield Static("[b]Options Misc2[/b]", classes="box", id="opts")
        # yield Label("Toggles",id="toggles",classes="label")
        yield Static("[b]General System Health[/b]", classes="box", id="gsh")
        yield Static("[b]System Alerts[/b]", classes="box", id="alrt")
        yield Static("[b]System Misc.[/b]", classes="box", id="msc")
        yield Horizontal(
            Button.success("DF Report"),
            Button.success("Scrub Stat"),
            Button.warning("ssh FF1"),
            Button.warning("ssh FN2"),
            Button.error("All Stop"),
            Button.error("Workers Stop"),
            Button("Primary", variant="primary"),
            Button.success("Blowjob"),
            Button.success("Success"),
            Button("Spooge"),
            Button("Butthole Bread"),
            Button("Banana"),
            Button("Fuck Off"),
            Button("Bitches"),
            Button("Cockring"),
            Button("Fast Validate"),
            Button("The Colonel"),
            Button("Whatever", variant="primary"),
        )

    # async def compose(self) -> ComposeResult:
    # """Composes the UI layout with a clock."""
    # yield Footer()
    # yield Header()
    #  yield ClockWidget()  # Add clock widget
    #  yield self.create_button_panel()


if __name__ == "__main__":
    app = GridLayoutTest()
    app.run()
