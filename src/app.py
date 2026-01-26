"""
Main Textual application for the Pomodoro TUI.
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Static, Button
from textual.binding import Binding
from rich.text import Text
from src.config import get_config
from src.utils.constants import APP_NAME, APP_VERSION


class WelcomeScreen(Static):
    """Welcome screen widget displaying app title and basic info."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static(
            f"[bold purple]{APP_NAME}[/bold purple]\n"
            f"[dim]Version {APP_VERSION}[/dim]\n\n"
            "[italic]An aesthetic Pomodoro timer for your terminal[/italic]\n\n"
            "Press [bold]Space[/bold] to start\n"
            "Press [bold]q[/bold] to quit\n"
            "Press [bold]?[/bold] for help",
            id="welcome-text"
        )


class PomodoroApp(App):
    """Main Pomodoro TUI application."""

    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }

    #welcome-text {
        width: auto;
        height: auto;
        padding: 2 4;
        border: heavy $primary;
        background: $panel;
        text-align: center;
    }

    Button {
        margin: 1 2;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("question_mark", "help", "Help"),
        Binding("c", "config", "Settings"),
    ]

    TITLE = APP_NAME

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.config = get_config()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            WelcomeScreen(),
            id="main-container"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        # Load configuration
        self.config.load()

        # Set theme if available
        theme = self.config.get("appearance", "theme", "textual-dark")
        try:
            self.theme = theme
        except Exception:
            # Theme not found, use default
            self.theme = "textual-dark"

    def action_help(self) -> None:
        """Show help screen."""
        self.notify("Help screen coming in Phase 9!", severity="information")

    def action_config(self) -> None:
        """Open configuration/settings."""
        self.notify("Settings panel coming in Phase 6!", severity="information")

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()


def run() -> None:
    """Run the Pomodoro TUI application."""
    app = PomodoroApp()
    app.run()


if __name__ == "__main__":
    run()
