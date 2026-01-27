"""
Settings panel for configuring timer and appearance options.
"""
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Label, Input
from textual.binding import Binding
from src.config import get_config
from src.utils.constants import (
    MIN_WORK_DURATION, MAX_WORK_DURATION,
    MIN_SHORT_BREAK_DURATION, MAX_SHORT_BREAK_DURATION,
    MIN_LONG_BREAK_DURATION, MAX_LONG_BREAK_DURATION,
    MIN_POMODOROS_UNTIL_LONG_BREAK, MAX_POMODOROS_UNTIL_LONG_BREAK,
)


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

    .setting-row {
        height: auto;
        width: 100%;
        margin: 0 0 1 0;
    }

    .setting-label {
        width: 30;
        padding: 0 1;
    }

    .setting-input {
        width: 10;
    }

    .setting-hint {
        width: 1fr;
        padding: 0 1;
    }
    """

    def __init__(self):
        """Initialize the settings panel."""
        super().__init__()
        self.modified = False
        self.config = get_config()

        # Load current settings
        self.work_duration = self.config.get("timer", "work_duration", 25)
        self.short_break = self.config.get("timer", "short_break_duration", 5)
        self.long_break = self.config.get("timer", "long_break_duration", 15)
        self.pomodoros_until_long = self.config.get("timer", "pomodoros_until_long_break", 4)

    def compose(self) -> ComposeResult:
        """Create child widgets for settings panel."""
        with Container(id="settings-container"):
            yield Static("Settings", id="settings-title")

            # Timer Settings Section
            with Vertical(classes="settings-section"):
                yield Label("Timer Settings", classes="section-title")

                # Work duration
                with Horizontal(classes="setting-row"):
                    yield Label("Work Duration:", classes="setting-label")
                    yield Input(
                        str(self.work_duration),
                        id="input-work-duration",
                        classes="setting-input",
                        type="integer"
                    )
                    yield Static(f"[dim]({MIN_WORK_DURATION}-{MAX_WORK_DURATION} min)[/dim]", classes="setting-hint")

                # Short break duration
                with Horizontal(classes="setting-row"):
                    yield Label("Short Break:", classes="setting-label")
                    yield Input(
                        str(self.short_break),
                        id="input-short-break",
                        classes="setting-input",
                        type="integer"
                    )
                    yield Static(f"[dim]({MIN_SHORT_BREAK_DURATION}-{MAX_SHORT_BREAK_DURATION} min)[/dim]", classes="setting-hint")

                # Long break duration
                with Horizontal(classes="setting-row"):
                    yield Label("Long Break:", classes="setting-label")
                    yield Input(
                        str(self.long_break),
                        id="input-long-break",
                        classes="setting-input",
                        type="integer"
                    )
                    yield Static(f"[dim]({MIN_LONG_BREAK_DURATION}-{MAX_LONG_BREAK_DURATION} min)[/dim]", classes="setting-hint")

                # Pomodoros until long break
                with Horizontal(classes="setting-row"):
                    yield Label("Pomodoros Until Long Break:", classes="setting-label")
                    yield Input(
                        str(self.pomodoros_until_long),
                        id="input-pomodoros",
                        classes="setting-input",
                        type="integer"
                    )
                    yield Static(f"[dim]({MIN_POMODOROS_UNTIL_LONG_BREAK}-{MAX_POMODOROS_UNTIL_LONG_BREAK})[/dim]", classes="setting-hint")

            # Buttons
            with Horizontal(id="settings-buttons"):
                yield Button("Save", id="btn-save", variant="success")
                yield Button("Cancel", id="btn-cancel", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "btn-save":
            if self._validate_and_save():
                self.dismiss(True)
        elif event.button.id == "btn-cancel":
            self.action_cancel()

    def _validate_and_save(self) -> bool:
        """
        Validate input values and save to config.

        Returns:
            True if validation passed and saved, False otherwise
        """
        try:
            # Get input values
            work_input = self.query_one("#input-work-duration", Input)
            short_input = self.query_one("#input-short-break", Input)
            long_input = self.query_one("#input-long-break", Input)
            pomodoros_input = self.query_one("#input-pomodoros", Input)

            work_duration = int(work_input.value)
            short_break = int(short_input.value)
            long_break = int(long_input.value)
            pomodoros = int(pomodoros_input.value)

            # Validate ranges
            if not (MIN_WORK_DURATION <= work_duration <= MAX_WORK_DURATION):
                self.app.notify(f"Work duration must be {MIN_WORK_DURATION}-{MAX_WORK_DURATION} minutes", severity="error")
                return False

            if not (MIN_SHORT_BREAK_DURATION <= short_break <= MAX_SHORT_BREAK_DURATION):
                self.app.notify(f"Short break must be {MIN_SHORT_BREAK_DURATION}-{MAX_SHORT_BREAK_DURATION} minutes", severity="error")
                return False

            if not (MIN_LONG_BREAK_DURATION <= long_break <= MAX_LONG_BREAK_DURATION):
                self.app.notify(f"Long break must be {MIN_LONG_BREAK_DURATION}-{MAX_LONG_BREAK_DURATION} minutes", severity="error")
                return False

            if not (MIN_POMODOROS_UNTIL_LONG_BREAK <= pomodoros <= MAX_POMODOROS_UNTIL_LONG_BREAK):
                self.app.notify(f"Pomodoros must be {MIN_POMODOROS_UNTIL_LONG_BREAK}-{MAX_POMODOROS_UNTIL_LONG_BREAK}", severity="error")
                return False

            # Save to config
            self.config.set("timer", "work_duration", work_duration)
            self.config.set("timer", "short_break_duration", short_break)
            self.config.set("timer", "long_break_duration", long_break)
            self.config.set("timer", "pomodoros_until_long_break", pomodoros)
            self.config.save()

            return True

        except ValueError:
            self.app.notify("Please enter valid numbers", severity="error")
            return False

    def action_cancel(self) -> None:
        """Cancel and close settings."""
        self.dismiss(False)
