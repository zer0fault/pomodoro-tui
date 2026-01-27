"""
Settings panel for configuring timer and appearance options.
"""
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Label
from textual.binding import Binding


class SettingsPanel(ModalScreen[bool]):
    """Modal screen for application settings."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
    ]

    CSS = """
    SettingsPanel {
        align: center middle;
    }

    #settings-container {
        width: 60;
        height: auto;
        background: $panel;
        border: heavy $primary;
        padding: 1 2;
    }

    #settings-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    .settings-section {
        margin: 1 0;
    }

    .section-title {
        text-style: bold;
        margin-bottom: 1;
    }

    #settings-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;
    }

    #settings-buttons Button {
        margin: 0 1;
    }
    """

    def __init__(self):
        """Initialize the settings panel."""
        super().__init__()
        self.modified = False

    def compose(self) -> ComposeResult:
        """Create child widgets for settings panel."""
        with Container(id="settings-container"):
            yield Static("Settings", id="settings-title")

            # Timer Settings Section
            with Vertical(classes="settings-section"):
                yield Label("Timer Settings", classes="section-title")
                yield Static("[dim]Timer duration settings will be added here[/dim]")

            # Buttons
            with Horizontal(id="settings-buttons"):
                yield Button("Save", id="btn-save", variant="success")
                yield Button("Cancel", id="btn-cancel", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "btn-save":
            self.dismiss(True)
        elif event.button.id == "btn-cancel":
            self.action_cancel()

    def action_cancel(self) -> None:
        """Cancel and close settings."""
        self.dismiss(False)
