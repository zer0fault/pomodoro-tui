"""
Integration tests for UI components and timer integration.
"""
import unittest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.timer import PomodoroTimer, TimerState
from src.components.timer_display import TimerDisplay
from src.components.progress_bar import PomodoroProgressBar


class TestTimerDisplay(unittest.TestCase):
    """Test TimerDisplay widget."""

    def test_timer_display_creation(self):
        """Test creating timer display widget."""
        display = TimerDisplay()
        self.assertIsNotNone(display)
        self.assertEqual(display.time_remaining, 0)
        self.assertEqual(display.current_phase, "IDLE")

    def test_set_time(self):
        """Test setting display time."""
        display = TimerDisplay()
        display.set_time(1500)  # 25 minutes
        self.assertEqual(display.time_remaining, 1500)

    def test_set_phase(self):
        """Test setting display phase."""
        display = TimerDisplay()
        display.set_phase("WORK")
        self.assertEqual(display.current_phase, "WORK")


class TestProgressBar(unittest.TestCase):
    """Test PomodoroProgressBar widget."""

    def test_progress_bar_creation(self):
        """Test creating progress bar."""
        bar = PomodoroProgressBar()
        self.assertIsNotNone(bar)
        self.assertEqual(bar.progress_value, 0.0)

    def test_set_progress(self):
        """Test setting progress."""
        bar = PomodoroProgressBar()
        bar.set_progress(0.5)
        self.assertEqual(bar.progress_value, 0.5)

    def test_progress_bounds(self):
        """Test progress stays within bounds."""
        bar = PomodoroProgressBar()

        bar.set_progress(-0.5)
        self.assertEqual(bar.progress_value, 0.0)

        bar.set_progress(1.5)
        self.assertEqual(bar.progress_value, 1.0)

    def test_get_percentage(self):
        """Test getting progress percentage."""
        bar = PomodoroProgressBar()
        bar.set_progress(0.75)
        self.assertEqual(bar.get_progress_percentage(), 75)


class TestTimerIntegration(unittest.TestCase):
    """Test timer integration with UI components."""

    def setUp(self):
        """Set up test fixtures."""
        self.timer = PomodoroTimer(work_duration=1)
        self.display = TimerDisplay()
        self.progress_bar = PomodoroProgressBar()

    def tearDown(self):
        """Clean up after tests."""
        if self.timer:
            self.timer.stop()

    def test_timer_to_display_integration(self):
        """Test updating display from timer."""
        # Start timer
        self.timer.start()

        # Update display with timer values
        self.display.set_time(self.timer.get_remaining_time())
        self.display.set_phase(self.timer.get_state().value)

        # Verify display updated
        self.assertEqual(self.display.time_remaining, 60)
        self.assertEqual(self.display.current_phase, "WORK")

        self.timer.stop()

    def test_timer_to_progress_bar_integration(self):
        """Test updating progress bar from timer."""
        self.timer.start()

        # Update progress bar
        progress = self.timer.get_progress()
        self.progress_bar.set_progress(progress)

        # Initial progress should be 0
        self.assertEqual(self.progress_bar.progress_value, 0.0)

        self.timer.stop()

    def test_timer_state_reflected_in_display(self):
        """Test display reflects timer state changes."""
        # IDLE state
        self.display.set_phase(self.timer.get_state().value)
        self.assertEqual(self.display.current_phase, "IDLE")

        # Start timer (WORK state)
        self.timer.start()
        self.display.set_phase(self.timer.get_state().value)
        self.assertEqual(self.display.current_phase, "WORK")

        # Pause timer
        self.timer.pause()
        self.display.set_phase(self.timer.get_state().value)
        self.assertEqual(self.display.current_phase, "PAUSED")

        self.timer.stop()


if __name__ == "__main__":
    unittest.main()
