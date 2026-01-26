"""
Configuration management for the Pomodoro TUI application.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional
import toml
from src.utils.constants import (
    CONFIG_DIR,
    CONFIG_FILE,
    DEFAULT_WORK_DURATION,
    DEFAULT_SHORT_BREAK_DURATION,
    DEFAULT_LONG_BREAK_DURATION,
    DEFAULT_POMODOROS_UNTIL_LONG_BREAK,
    DEFAULT_THEME,
    DEFAULT_VOLUME,
    DEFAULT_AUDIO_ENABLED,
    ART_STYLE_TOMATO,
)


class Config:
    """Manages application configuration loading, saving, and access."""

    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = Path(CONFIG_DIR).expanduser()
        self.config_path = self.config_dir / CONFIG_FILE
        self.config_data: Dict[str, Any] = {}
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get the default configuration dictionary.

        Returns:
            Default configuration dictionary
        """
        return {
            "timer": {
                "work_duration": DEFAULT_WORK_DURATION,
                "short_break_duration": DEFAULT_SHORT_BREAK_DURATION,
                "long_break_duration": DEFAULT_LONG_BREAK_DURATION,
                "pomodoros_until_long_break": DEFAULT_POMODOROS_UNTIL_LONG_BREAK,
                "auto_start_breaks": False,
                "auto_start_work": False,
            },
            "appearance": {
                "theme": DEFAULT_THEME,
                "show_ascii_art": True,
                "ascii_art_style": ART_STYLE_TOMATO,
                "show_progress_bar": True,
                "show_session_count": True,
                "animations_enabled": True,
            },
            "audio": {
                "enabled": DEFAULT_AUDIO_ENABLED,
                "volume": DEFAULT_VOLUME,
                "work_complete_sound": "complete.wav",
                "break_complete_sound": "break.wav",
            },
            "statistics": {
                "track_sessions": True,
                "save_history": True,
                "history_file": "~/.pomodoro-tui/history.json",
            },
        }

    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default.

        Returns:
            Configuration dictionary
        """
        if self.config_path.exists():
            try:
                self.config_data = toml.load(self.config_path)
                # Merge with defaults to ensure all keys exist
                default_config = self._get_default_config()
                for section, values in default_config.items():
                    if section not in self.config_data:
                        self.config_data[section] = values
                    else:
                        for key, value in values.items():
                            if key not in self.config_data[section]:
                                self.config_data[section][key] = value
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                self.config_data = self._get_default_config()
        else:
            self.config_data = self._get_default_config()
            self.save()

        return self.config_data

    def save(self) -> bool:
        """
        Save current configuration to file.

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_path, "w") as f:
                toml.dump(self.config_data, f)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration value.

        Args:
            section: Configuration section (e.g., 'timer', 'appearance')
            key: Configuration key within the section
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if not self.config_data:
            self.load()

        return self.config_data.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set a specific configuration value.

        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if not self.config_data:
            self.load()

        if section not in self.config_data:
            self.config_data[section] = {}

        self.config_data[section][key] = value

    def update(self, updates: Dict[str, Dict[str, Any]]) -> bool:
        """
        Update configuration with new values and save.

        Args:
            updates: Dictionary of section -> {key: value} updates

        Returns:
            True if successful, False otherwise
        """
        if not self.config_data:
            self.load()

        for section, values in updates.items():
            if section not in self.config_data:
                self.config_data[section] = {}
            self.config_data[section].update(values)

        return self.save()

    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values.

        Returns:
            True if successful, False otherwise
        """
        self.config_data = self._get_default_config()
        return self.save()


# Global config instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Global Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
        _config_instance.load()
    return _config_instance


def load_config() -> Dict[str, Any]:
    """
    Load and return configuration dictionary.

    Returns:
        Configuration dictionary
    """
    return get_config().load()


def save_config() -> bool:
    """
    Save current configuration.

    Returns:
        True if successful, False otherwise
    """
    return get_config().save()


def get_config_value(section: str, key: str, default: Any = None) -> Any:
    """
    Get a specific configuration value.

    Args:
        section: Configuration section
        key: Configuration key
        default: Default value if not found

    Returns:
        Configuration value
    """
    return get_config().get(section, key, default)


def update_config(updates: Dict[str, Dict[str, Any]]) -> bool:
    """
    Update configuration with new values.

    Args:
        updates: Dictionary of updates

    Returns:
        True if successful, False otherwise
    """
    return get_config().update(updates)


def reset_config() -> bool:
    """
    Reset configuration to defaults.

    Returns:
        True if successful, False otherwise
    """
    return get_config().reset_to_defaults()
