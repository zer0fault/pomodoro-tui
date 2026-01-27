"""
Theme management for Pomodoro TUI.
Handles loading, switching, and persisting themes.
"""
from pathlib import Path
from typing import Dict, List, Optional


class ThemeManager:
    """Manages theme loading and switching."""

    # Available themes with their display names
    THEMES = {
        "pomodoro-default": "Default Purple",
        "pomodoro-catppuccin": "Catppuccin (Mocha)",
        "pomodoro-nord": "Nord",
        "pomodoro-gruvbox": "Gruvbox",
        "pomodoro-tokyo-night": "Tokyo Night",
    }

    def __init__(self, themes_dir: Optional[Path] = None):
        """
        Initialize the theme manager.

        Args:
            themes_dir: Path to themes directory. If None, uses default location.
        """
        if themes_dir is None:
            # Default to themes/ directory in project root
            project_root = Path(__file__).parent.parent
            self.themes_dir = project_root / "themes"
        else:
            self.themes_dir = Path(themes_dir)

        self.current_theme = "pomodoro-default"
        self._theme_cache: Dict[str, str] = {}

    def get_available_themes(self) -> Dict[str, str]:
        """
        Get dictionary of available themes.

        Returns:
            Dictionary mapping theme IDs to display names.
        """
        available = {}
        for theme_id, display_name in self.THEMES.items():
            theme_path = self.themes_dir / f"{theme_id}.tcss"
            if theme_path.exists():
                available[theme_id] = display_name
        return available

    def get_theme_list(self) -> List[tuple[str, str]]:
        """
        Get list of available themes as (id, name) tuples.

        Returns:
            List of (theme_id, display_name) tuples.
        """
        return list(self.get_available_themes().items())

    def load_theme(self, theme_id: str) -> Optional[str]:
        """
        Load a theme's CSS content.

        Args:
            theme_id: ID of the theme to load (e.g., "pomodoro-default")

        Returns:
            Theme CSS content as string, or None if theme not found.
        """
        # Check cache first
        if theme_id in self._theme_cache:
            return self._theme_cache[theme_id]

        theme_path = self.themes_dir / f"{theme_id}.tcss"
        if not theme_path.exists():
            return None

        try:
            with open(theme_path, "r", encoding="utf-8") as f:
                css_content = f.read()
                self._theme_cache[theme_id] = css_content
                return css_content
        except Exception as e:
            print(f"Error loading theme {theme_id}: {e}")
            return None

    def get_theme_path(self, theme_id: str) -> Optional[Path]:
        """
        Get the file path for a theme.

        Args:
            theme_id: ID of the theme

        Returns:
            Path to theme file, or None if not found.
        """
        theme_path = self.themes_dir / f"{theme_id}.tcss"
        if theme_path.exists():
            return theme_path
        return None

    def set_current_theme(self, theme_id: str) -> bool:
        """
        Set the current theme.

        Args:
            theme_id: ID of the theme to set as current

        Returns:
            True if theme was set successfully, False otherwise.
        """
        if theme_id in self.THEMES and self.get_theme_path(theme_id):
            self.current_theme = theme_id
            return True
        return False

    def get_current_theme(self) -> str:
        """
        Get the ID of the current theme.

        Returns:
            Current theme ID.
        """
        return self.current_theme

    def get_current_theme_name(self) -> str:
        """
        Get the display name of the current theme.

        Returns:
            Current theme display name.
        """
        return self.THEMES.get(self.current_theme, "Unknown")

    def get_next_theme(self) -> str:
        """
        Get the next theme in the list (for cycling).

        Returns:
            Next theme ID.
        """
        available = list(self.get_available_themes().keys())
        if not available:
            return self.current_theme

        try:
            current_index = available.index(self.current_theme)
            next_index = (current_index + 1) % len(available)
            return available[next_index]
        except ValueError:
            # Current theme not in available list, return first
            return available[0]

    def get_previous_theme(self) -> str:
        """
        Get the previous theme in the list (for cycling).

        Returns:
            Previous theme ID.
        """
        available = list(self.get_available_themes().keys())
        if not available:
            return self.current_theme

        try:
            current_index = available.index(self.current_theme)
            prev_index = (current_index - 1) % len(available)
            return available[prev_index]
        except ValueError:
            # Current theme not in available list, return last
            return available[-1]

    def clear_cache(self) -> None:
        """Clear the theme cache."""
        self._theme_cache.clear()


# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """
    Get the global theme manager instance.

    Returns:
        ThemeManager instance.
    """
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
