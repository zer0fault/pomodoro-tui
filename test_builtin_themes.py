"""Test Textual's built-in theme switching."""
from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Container

class ThemeTestApp(App):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("Current theme test", id="test"),
            Button("Switch to Nord", id="nord"),
            Button("Switch to Gruvbox", id="gruvbox"),
            Button("Switch to Catppuccin", id="catppuccin"),
        )

    def on_mount(self):
        print(f"Current theme: {self.theme}")
        print(f"Available: {list(self.available_themes)[:5]}...")

    def on_button_pressed(self, event: Button.Pressed):
        theme_map = {
            "nord": "nord",
            "gruvbox": "gruvbox",
            "catppuccin": "catppuccin-mocha",
        }
        if event.button.id in theme_map:
            new_theme = theme_map[event.button.id]
            print(f"Switching to: {new_theme}")
            self.theme = new_theme
            print(f"Theme is now: {self.theme}")

if __name__ == "__main__":
    app = ThemeTestApp()
    app.run()
