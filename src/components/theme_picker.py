"""
Theme picker widget for selecting and previewing themes.
"""
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Static, OptionList
from textual.widgets.option_list import Option
from textual.binding import Binding

from src.theme_manager import get_theme_manager


class ThemePicker(ModalScreen[str]):
    """Modal screen for picking a theme with full keyboard support."""

    CSS = """
    ThemePicker {
        align: center middle;
    }

    #theme-picker-container {
        width: 60;
        height: auto;
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
        height: 12;
        border: solid $primary;
        margin: 1 0;
    }

    #theme-picker-help {
        width: 100%;
        text-align: center;
        color: $text-muted;
        margin-top: 1;
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
        Binding("escape", "cancel", "Cancel", priority=True),
        Binding("enter", "apply", "Apply", priority=True),
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

            # Create OptionList with themes
            option_list = OptionList(id="theme-list")
            yield option_list

            yield Static(
                "[dim]↑↓[/dim] Navigate  •  [dim]Enter[/dim] Apply  •  [dim]Esc[/dim] Cancel",
                id="theme-picker-help"
            )

            with Horizontal(id="theme-picker-buttons"):
                yield Button("Apply", id="btn-apply", variant="success")
                yield Button("Cancel", id="btn-cancel", variant="default")

    def on_mount(self) -> None:
        """Populate the option list when mounted."""
        option_list = self.query_one("#theme-list", OptionList)
        current_theme = self.theme_manager.get_current_theme()

        # Add themes to option list
        highlighted_index = 0
        for index, (theme_id, theme_name) in enumerate(self.theme_manager.get_theme_list()):
            # Mark current theme with ●
            prefix = "● " if theme_id == current_theme else "  "
            option_list.add_option(Option(f"{prefix}{theme_name}", id=theme_id))

            if theme_id == current_theme:
                highlighted_index = index

        # Highlight the current theme
        option_list.highlighted = highlighted_index

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle theme selection from option list."""
        if event.option.id:
            self.selected_theme = event.option.id
            # Apply immediately when selected with Enter in the list
            self.dismiss(self.selected_theme)

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        """Update selected theme as user navigates with arrow keys."""
        if event.option.id:
            self.selected_theme = event.option.id

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "btn-apply":
            self.action_apply()
        elif event.button.id == "btn-cancel":
            self.action_cancel()

    def action_apply(self) -> None:
        """Apply the selected theme."""
        self.dismiss(self.selected_theme)

    def action_cancel(self) -> None:
        """Cancel without applying changes."""
        self.dismiss(None)
