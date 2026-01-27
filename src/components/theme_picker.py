"""
Theme picker widget for selecting and previewing themes.
"""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from textual.binding import Binding

from src.theme_manager import get_theme_manager


class ThemeOption(Static):
    """A single theme option in the picker."""

    def __init__(self, theme_id: str, theme_name: str, is_current: bool = False):
        """
        Initialize theme option.

        Args:
            theme_id: Theme identifier
            theme_name: Display name of theme
            is_current: Whether this is the currently selected theme
        """
        super().__init__()
        self.theme_id = theme_id
        self.theme_name = theme_name
        self.is_current = is_current

    def compose(self) -> ComposeResult:
        """Compose the theme option."""
        current_marker = "● " if self.is_current else "  "
        yield Label(f"{current_marker}{self.theme_name}")

    def on_click(self) -> None:
        """Handle click on theme option."""
        # Post a custom message that the parent can handle
        self.post_message(ThemeSelected(self.theme_id))


class ThemeSelected(Static.Changed):
    """Message posted when a theme is selected."""

    def __init__(self, theme_id: str) -> None:
        """
        Initialize message.

        Args:
            theme_id: ID of selected theme
        """
        super().__init__()
        self.theme_id = theme_id


class ThemePicker(ModalScreen[str]):
    """Modal screen for picking a theme."""

    CSS = """
    ThemePicker {
        align: center middle;
    }

    #theme-picker-container {
        width: 50;
        height: auto;
        max-height: 20;
        background: $panel;
        border: thick $primary;
        padding: 1 2;
    }

    #theme-picker-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    #theme-list {
        width: 100%;
        height: auto;
        max-height: 10;
        border: solid $primary;
        padding: 1;
        margin: 1 0;
    }

    ThemeOption {
        width: 100%;
        height: auto;
        padding: 0 1;
        margin: 0;
    }

    ThemeOption:hover {
        background: $primary-lighten-1;
        color: $surface;
    }

    ThemeOption Label {
        width: 100%;
    }

    #theme-picker-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;
    }

    #theme-picker-buttons Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("escape", "dismiss_picker", "Cancel", priority=True),
        Binding("t", "dismiss_picker", "Close", priority=True),
    ]

    def __init__(self):
        """Initialize the theme picker."""
        super().__init__()
        self.theme_manager = get_theme_manager()
        self.selected_theme = self.theme_manager.get_current_theme()

    def compose(self) -> ComposeResult:
        """Compose the theme picker UI."""
        with Container(id="theme-picker-container"):
            yield Static("Theme Selector", id="theme-picker-title")

            with VerticalScroll(id="theme-list"):
                current_theme = self.theme_manager.get_current_theme()
                for theme_id, theme_name in self.theme_manager.get_theme_list():
                    is_current = (theme_id == current_theme)
                    yield ThemeOption(theme_id, theme_name, is_current)

            with Container(id="theme-picker-buttons"):
                yield Button("Apply", id="btn-apply", variant="success")
                yield Button("Cancel", id="btn-cancel", variant="default")

    def on_theme_option_click(self, event: ThemeOption.Changed) -> None:
        """Handle theme option selection."""
        # Update visual selection
        for option in self.query(ThemeOption):
            option.is_current = (option.theme_id == event.control.theme_id)
            option.refresh()

    def on_theme_selected(self, message: ThemeSelected) -> None:
        """Handle theme selection."""
        self.selected_theme = message.theme_id

        # Update visual markers
        for option in self.query(ThemeOption):
            option.is_current = (option.theme_id == self.selected_theme)
            option.remove_class("selected")
            if option.is_current:
                option.add_class("selected")
            # Force re-compose to update marker
            label = option.query_one(Label)
            current_marker = "● " if option.is_current else "  "
            label.update(f"{current_marker}{option.theme_name}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "btn-apply":
            # Apply the selected theme
            self.dismiss(self.selected_theme)
        elif event.button.id == "btn-cancel":
            # Cancel without applying
            self.dismiss(None)

    def action_dismiss_picker(self) -> None:
        """Dismiss the picker without applying changes."""
        self.dismiss(None)
