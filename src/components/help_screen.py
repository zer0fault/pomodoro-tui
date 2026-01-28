"""
Help screen displaying keyboard shortcuts and usage information.
"""
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button
from textual.binding import Binding


class HelpScreen(ModalScreen[None]):
    """Modal screen showing keyboard shortcuts and help information."""

    BINDINGS = [
        Binding("escape", "close", "Close", priority=True),
        Binding("question_mark", "close", "Close", priority=True),
    ]

    CSS = """
    HelpScreen {
        align: center middle;
    }

    #help-container {
        width: 70;
        height: auto;
        max-height: 90%;
        background: $panel;
        border: heavy $primary;
        padding: 1 2;
    }

    #help-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #help-content {
        height: auto;
        max-height: 30;
    }

    .help-section {
        margin: 1 0;
    }

    .section-title {
        text-style: bold;
        margin-bottom: 1;
    }

    .shortcut-row {
        margin: 0 0 0 2;
    }

    #help-footer {
        text-align: center;
        margin-top: 1;
    }

    #help-close-btn {
        width: 100%;
        align: center middle;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for help screen."""
        with Container(id="help-container"):
            yield Static("Pomodoro TUI - Help", id="help-title")

            with ScrollableContainer(id="help-content"):
                # Timer Controls
                with Vertical(classes="help-section"):
                    yield Static("Timer Controls", classes="section-title")
                    yield Static("[dim]Space[/dim]  Start/Pause timer", classes="shortcut-row")
                    yield Static("[dim]S[/dim]      Stop and reset timer", classes="shortcut-row")
                    yield Static("[dim]N[/dim]      Skip to next phase", classes="shortcut-row")

                # Settings & Customization
                with Vertical(classes="help-section"):
                    yield Static("Settings & Customization", classes="section-title")
                    yield Static("[dim]C[/dim]      Open settings panel", classes="shortcut-row")
                    yield Static("[dim]T[/dim]      Open theme picker", classes="shortcut-row")

                # Application
                with Vertical(classes="help-section"):
                    yield Static("Application", classes="section-title")
                    yield Static("[dim]?[/dim]      Show this help screen", classes="shortcut-row")
                    yield Static("[dim]Q[/dim]      Quit application", classes="shortcut-row")

                # Timer Phases
                with Vertical(classes="help-section"):
                    yield Static("Timer Phases", classes="section-title")
                    yield Static("Work sessions turn the timer border [bold red]red[/bold red]", classes="shortcut-row")
                    yield Static("Break sessions turn the timer border [bold green]green[/bold green]", classes="shortcut-row")

                # About
                with Vertical(classes="help-section"):
                    yield Static("About", classes="section-title")
                    yield Static("Pomodoro TUI - A minimalistic terminal timer", classes="shortcut-row")
                    yield Static("Built with Textual framework", classes="shortcut-row")

            with Horizontal(id="help-close-btn"):
                yield Button("Close", id="btn-close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "btn-close":
            self.action_close()

    def action_close(self) -> None:
        """Close the help screen."""
        self.dismiss()
