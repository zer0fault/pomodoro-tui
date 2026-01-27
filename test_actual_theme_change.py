"""
Test that theme actually changes by checking widget styles.
"""
import sys
import io
from time import sleep

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from textual.app import App, ComposeResult
from textual.widgets import Button
from pathlib import Path

# Simple test app
class TestApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    Button {
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Button("Test", id="test-btn")

    def on_mount(self):
        # Load initial theme
        theme_path = Path("themes/pomodoro-catppuccin.tcss")
        self.__class__.STYLESHEETS = [str(theme_path)]
        self.refresh_css()

        print(f"Initial STYLESHEETS: {self.STYLESHEETS}")
        print(f"Initial stylesheet rules: {len(self.stylesheet.rules)}")

        # Try switching
        self.set_timer(1, self.switch_theme)
        self.set_timer(2, self.check_and_exit)

    def switch_theme(self):
        print("\n--- Switching to Nord ---")
        theme_path = Path("themes/pomodoro-nord.tcss")
        self.__class__.STYLESHEETS = [str(theme_path)]
        self.refresh_css()
        print(f"New STYLESHEETS: {self.STYLESHEETS}")
        print(f"New stylesheet rules: {len(self.stylesheet.rules)}")

    def check_and_exit(self):
        print("\n--- Final Check ---")
        print(f"STYLESHEETS: {self.STYLESHEETS}")
        print(f"Rules count: {len(self.stylesheet.rules)}")
        print("\nIf rules count is same, refresh_css() is NOT reloading from STYLESHEETS")
        self.exit()


if __name__ == "__main__":
    app = TestApp()
    app.run()
