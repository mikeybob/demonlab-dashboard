from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Digits, Rule


class ClockApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #clock {
        border: double green;
        content-align: center middle;
        text-align: center;
        width: 100;
    }
    Rule {
        width: auto;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        # yield Rule(line_style="thick", id="hrule1")
        yield Digits("", id="clock")
        # yield Rule(line_style="thick", id="hrule2")

    def on_ready(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")


if __name__ == "__main__":
    app = ClockApp()
    app.run(inline=True)
