"""
ASCII art display widget for the Pomodoro TUI.
"""
from pathlib import Path
from textual.widgets import Static
from textual.reactive import reactive


class ArtDisplay(Static):
    """Widget for displaying ASCII art."""

    art_content = reactive("")

    def __init__(self, *args, **kwargs):
        """Initialize the art display widget."""
        super().__init__(*args, **kwargs)
        self.assets_path = Path(__file__).parent.parent.parent / "assets" / "art"

    def load_art(self, art_name: str) -> None:
        """
        Load ASCII art from a file.

        Args:
            art_name: Name of the art file (without .txt extension)
        """
        art_file = self.assets_path / f"{art_name}.txt"

        try:
            if art_file.exists():
                with open(art_file, "r", encoding="utf-8") as f:
                    self.art_content = f.read()
            else:
                self.art_content = f"[dim]Art file not found: {art_name}[/dim]"
        except Exception as e:
            self.art_content = f"[dim]Error loading art: {e}[/dim]"

    def watch_art_content(self, new_content: str) -> None:
        """Update the display when art content changes."""
        self.update(new_content)
