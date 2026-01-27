"""
Audio notification manager for the Pomodoro TUI.
"""
import winsound
from typing import Optional
from src.config import get_config


class AudioManager:
    """Manages audio notifications and sound playback."""

    def __init__(self):
        """Initialize the audio manager."""
        self.config = get_config()
        self.enabled = self.config.get("audio", "enabled", True)
        self.volume = self.config.get("audio", "volume", 0.7)

    def play_work_complete(self) -> None:
        """Play notification sound for completed work session."""
        if not self.enabled:
            return

        try:
            # Play a pleasant two-tone beep (frequency, duration in ms)
            winsound.Beep(800, 200)  # Higher pitch
            winsound.Beep(600, 300)  # Lower pitch
        except Exception as e:
            print(f"Error playing work complete sound: {e}")

    def play_break_complete(self) -> None:
        """Play notification sound for completed break."""
        if not self.enabled:
            return

        try:
            # Play a single tone beep
            winsound.Beep(600, 400)
        except Exception as e:
            print(f"Error playing break complete sound: {e}")

    def play_timer_start(self) -> None:
        """Play notification sound when timer starts."""
        if not self.enabled:
            return

        try:
            # Play a quick beep
            winsound.Beep(700, 100)
        except Exception as e:
            print(f"Error playing timer start sound: {e}")

    def set_enabled(self, enabled: bool) -> None:
        """
        Enable or disable audio notifications.

        Args:
            enabled: True to enable audio, False to disable
        """
        self.enabled = enabled
        self.config.set("audio", "enabled", enabled)
        self.config.save()

    def set_volume(self, volume: float) -> None:
        """
        Set audio volume (note: winsound doesn't support volume control).

        Args:
            volume: Volume level between 0.0 and 1.0
        """
        self.volume = max(0.0, min(1.0, volume))
        self.config.set("audio", "volume", self.volume)
        self.config.save()

    def toggle_enabled(self) -> bool:
        """
        Toggle audio enabled/disabled.

        Returns:
            New enabled state
        """
        self.enabled = not self.enabled
        self.config.set("audio", "enabled", self.enabled)
        self.config.save()
        return self.enabled


# Global audio manager instance
_audio_manager: Optional[AudioManager] = None


def get_audio_manager() -> AudioManager:
    """
    Get the global audio manager instance.

    Returns:
        Global AudioManager instance
    """
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioManager()
    return _audio_manager
