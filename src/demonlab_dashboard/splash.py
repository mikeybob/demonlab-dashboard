#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
from time import time

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Center, Middle
from textual.widgets import Label, Static

try:
    from pyfiglet import Figlet
    has_figlet = True
except ImportError:
    has_figlet = False

class BeamTitle(Static):
    """Main title with beam column effect"""
    def on_mount(self) -> None:
        self.base_text = self.renderable
        self.beam_columns()

    def beam_columns(self) -> None:
        """Create vertical beam effect by highlighting columns"""
        lines = str(self.base_text).split('\n')
        max_len = max(len(line) for line in lines)

        # Randomly select columns to highlight
        beam_cols = [i for i in range(max_len) if random.random() < 0.3]

        # Build highlighted text
        new_text = []
        for line in lines:
            highlighted = []
            for i, char in enumerate(line):
                if i in beam_cols:
                    highlighted.append(f"[#ffff00]{char}[/]")
                else:
                    highlighted.append(f"[#00ffff]{char}[/]")
            new_text.append("".join(highlighted))

        self.update("\n".join(new_text))
        self.set_timer(0.2, self.beam_columns)

class ShimmerSubtitle(Static):
    """Subtitle with shimmer effect"""
    def on_mount(self) -> None:
        self.base_text = self.renderable
        self.shimmer_text()

    def shimmer_text(self) -> None:
        """Create random character shimmer effect"""
        text = str(self.base_text)
        shimmered = []
        for char in text:
            if random.random() < 0.15:
                shimmered.append(f"[bold #ffffff]{char}[/]")
            else:
                shimmered.append(f"[#aaaaaa]{char}[/]")
        self.update("".join(shimmered))
        self.set_timer(0.15, self.shimmer_text)

class SplashEffect(App):
    CSS = """
    Screen {
        background: #000020;
        color: #00ffff;
    }

    .main-title {
        text-align: center;
        width: 100%;
        margin-bottom: 2;
    }

    .subtitle {
        text-align: center;
        width: 100%;
        margin-top: 1;
    }

    .footer {
        text-align: center;
        width: 100%;
        margin-top: 4;
        color: #555577;
    }
    """

    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                if has_figlet:
                    fig = Figlet(font='5x8', width=120)
                    title_text = fig.renderText("DEMONLAB DASHBOARD")
                    yield BeamTitle(title_text, classes="main-title")
                else:
                    yield BeamTitle("DEMONLAB DASHBOARD", classes="main-title")

                yield ShimmerSubtitle("HOMELAB CONTROL PANEL", classes="subtitle")
                yield ShimmerSubtitle("Initializing subsystems...", classes="footer")

    def on_mount(self) -> None:
        self.set_timer(15.0, self.exit_splash)

    def exit_splash(self) -> None:
        self.exit("Splash complete")

if __name__ == "__main__":
    app = SplashEffect()
    app.run()
