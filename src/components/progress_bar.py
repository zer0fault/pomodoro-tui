"""
Custom progress bar widget for Pomodoro timer.
"""
from textual.widgets import ProgressBar
from textual.reactive import reactive


class PomodoroProgressBar(ProgressBar):
    """
    Progress bar showing session completion progress.

    Displays progress with smooth updates and percentage.
    """

    progress_value = reactive(0.0)
    show_percentage = reactive(True)

    def __init__(self, *args, **kwargs):
        """Initialize the progress bar."""
        super().__init__(*args, **kwargs)
        self.total = 100
        self.show_percentage = False  # Hide percentage text to avoid duplication with timer

    def watch_progress_value(self, new_value: float) -> None:
        """Called when progress_value changes."""
        # Update the actual progress (0-100)
        self.update(progress=new_value * 100)

    def set_progress(self, progress: float) -> None:
        """
        Set progress value.

        Args:
            progress: Progress as float between 0.0 and 1.0
        """
        self.progress_value = max(0.0, min(1.0, progress))

    def get_progress_percentage(self) -> int:
        """
        Get current progress as percentage.

        Returns:
            Progress percentage (0-100)
        """
        return int(self.progress_value * 100)
