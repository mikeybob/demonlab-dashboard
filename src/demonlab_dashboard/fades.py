from textual.screen import Screen
from textual.widgets import Static
import asyncio

class FadingScreen(Screen):

    def compose(self):
        self.static = Static("Welcome to the Fading Screen")
        self.opacity = 0.0  # Start invisible
        self.static.styles.opacity = self.opacity
        return self.static

    async def fade_in(self):
        while self.opacity < 1.0:
            self.opacity += 0.1
            self.static.styles.opacity = self.opacity
            await asyncio.sleep(0.05)

    async def fade_out(self):
        while self.opacity < 0.0:
            self.opacity -= 0.1
            self.static.styles.opacity = self.opacity
            await asyncio.sleep(0.05)

    async def on_mount(self):
        # Fade in the screen upon mounting
        await self.fade_in()

    async def on_button_click(self, event):
        # Example of fading out before a transition
        await self.fade_out()
        await self.app.pop_screen()
