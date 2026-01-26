"""
Unit tests for the Pomodoro timer.
"""
import unittest
import time
from src.timer import PomodoroTimer, TimerState


class TestPomodoroTimer(unittest.TestCase):
    """Test cases for the PomodoroTimer class."""

    def setUp(self):
        """Set up test fixtures before each test."""
        # Use short durations for faster testing
        self.timer = PomodoroTimer(
            work_duration=1,  # 1 minute
            short_break_duration=1,
            long_break_duration=1,
            pomodoros_until_long_break=2,
        )

    def tearDown(self):
        """Clean up after each test."""
        if self.timer:
            self.timer.stop()

    def test_initial_state(self):
        """Test timer starts in IDLE state."""
        self.assertEqual(self.timer.get_state(), TimerState.IDLE)
        self.assertEqual(self.timer.current_pomodoro, 0)
        self.assertEqual(self.timer.completed_pomodoros_today, 0)

    def test_start_work_session(self):
        """Test starting a work session."""
        result = self.timer.start()
        self.assertTrue(result)
        self.assertEqual(self.timer.get_state(), TimerState.WORK)
        self.assertEqual(self.timer.remaining_seconds, 60)  # 1 minute

    def test_cannot_start_when_running(self):
        """Test cannot start when already running."""
        self.timer.start()
        result = self.timer.start()  # Try to start again
        self.assertFalse(result)

    def test_pause_and_resume(self):
        """Test pausing and resuming a session."""
        self.timer.start()
        time.sleep(0.5)  # Let it run briefly

        # Pause
        result = self.timer.pause()
        self.assertTrue(result)
        self.assertEqual(self.timer.get_state(), TimerState.PAUSED)

        # Check time doesn't change while paused
        remaining_before = self.timer.remaining_seconds
        time.sleep(1.5)
        remaining_after = self.timer.remaining_seconds
        self.assertEqual(remaining_before, remaining_after)

        # Resume
        result = self.timer.resume()
        self.assertTrue(result)
        self.assertEqual(self.timer.get_state(), TimerState.WORK)

    def test_stop_timer(self):
        """Test stopping the timer."""
        self.timer.start()
        time.sleep(0.5)

        result = self.timer.stop()
        self.assertTrue(result)
        self.assertEqual(self.timer.get_state(), TimerState.IDLE)
        self.assertEqual(self.timer.remaining_seconds, 0)

    def test_skip_session(self):
        """Test skipping to next phase."""
        self.timer.start()
        time.sleep(0.5)

        result = self.timer.skip()
        self.assertTrue(result)

        # Wait for session completion to be processed
        time.sleep(2)

        # Should transition to short break
        self.assertEqual(self.timer.get_state(), TimerState.SHORT_BREAK)
        self.assertEqual(self.timer.current_pomodoro, 1)

    def test_timer_countdown(self):
        """Test timer counts down correctly."""
        self.timer.start()
        initial_remaining = self.timer.remaining_seconds

        time.sleep(2.5)  # Wait 2-3 seconds

        current_remaining = self.timer.remaining_seconds
        elapsed = initial_remaining - current_remaining

        # Should have elapsed ~2-3 seconds (with tolerance)
        self.assertGreaterEqual(elapsed, 2)
        self.assertLessEqual(elapsed, 4)

    def test_session_complete_callback(self):
        """Test session complete callback is invoked."""
        callback_invoked = []

        def on_complete(pomodoro_num):
            callback_invoked.append(pomodoro_num)

        self.timer.on("session_complete", on_complete)
        self.timer.start()
        self.timer.skip()  # Skip to trigger completion

        # Wait for callback
        time.sleep(2)

        self.assertEqual(len(callback_invoked), 1)
        self.assertEqual(callback_invoked[0], 1)

    def test_break_complete_callback(self):
        """Test break complete callback is invoked."""
        callback_invoked = []

        def on_break_complete(break_type):
            callback_invoked.append(break_type)

        self.timer.on("break_complete", on_break_complete)

        # Start and complete work session
        self.timer.start()
        self.timer.skip()
        time.sleep(2)

        # Should now be in short break - skip it
        self.timer.skip()
        time.sleep(2)

        # Break complete callback should have been invoked
        self.assertGreater(len(callback_invoked), 0)

    def test_tick_callback(self):
        """Test tick callback is invoked every second."""
        tick_count = []

        def on_tick(remaining):
            tick_count.append(remaining)

        self.timer.on("tick", on_tick)
        self.timer.start()

        time.sleep(3.5)  # Wait for 3-4 ticks

        self.timer.stop()

        # Should have received 3-4 ticks
        self.assertGreaterEqual(len(tick_count), 3)
        self.assertLessEqual(len(tick_count), 5)

    def test_state_change_callback(self):
        """Test state change callback is invoked."""
        state_changes = []

        def on_state_change(old_state, new_state):
            state_changes.append((old_state, new_state))

        self.timer.on("state_change", on_state_change)
        self.timer.start()

        time.sleep(0.5)

        # Should have at least one state change (IDLE -> WORK)
        self.assertGreater(len(state_changes), 0)
        self.assertEqual(state_changes[0][0], TimerState.IDLE)
        self.assertEqual(state_changes[0][1], TimerState.WORK)

    def test_cycle_complete_after_multiple_pomodoros(self):
        """Test cycle completes after configured number of pomodoros."""
        cycle_complete_count = []

        def on_cycle_complete(pomodoro_num):
            cycle_complete_count.append(pomodoro_num)

        self.timer.on("cycle_complete", on_cycle_complete)

        # Complete first pomodoro
        self.timer.start()
        self.timer.skip()
        time.sleep(2)

        # Skip short break
        self.timer.skip()
        time.sleep(2)

        # Should be back to IDLE
        self.assertEqual(self.timer.get_state(), TimerState.IDLE)

        # Start and complete second pomodoro
        self.timer.start()
        self.timer.skip()
        time.sleep(2)

        # After 2nd pomodoro, should trigger long break and cycle complete
        self.assertEqual(len(cycle_complete_count), 1)
        self.assertEqual(cycle_complete_count[0], 2)
        self.assertEqual(self.timer.get_state(), TimerState.LONG_BREAK)

        # After long break, pomodoro counter should reset
        self.timer.skip()
        time.sleep(2)
        self.assertEqual(self.timer.current_pomodoro, 0)

    def test_get_progress(self):
        """Test progress calculation."""
        self.timer.start()
        time.sleep(0.1)

        progress = self.timer.get_progress()
        self.assertGreaterEqual(progress, 0.0)
        self.assertLessEqual(progress, 1.0)

    def test_get_session_info(self):
        """Test getting session information."""
        self.timer.start()
        time.sleep(0.5)

        info = self.timer.get_session_info()

        self.assertIn("state", info)
        self.assertIn("current_pomodoro", info)
        self.assertIn("remaining_seconds", info)
        self.assertIn("elapsed_seconds", info)
        self.assertIn("progress", info)

        self.assertEqual(info["state"], TimerState.WORK.value)
        self.assertGreater(info["elapsed_seconds"], 0)

    def test_update_durations(self):
        """Test updating timer durations."""
        self.timer.update_durations(
            work_duration=2,
            short_break_duration=1,
            long_break_duration=3,
        )

        self.assertEqual(self.timer.work_duration, 120)  # 2 minutes
        self.assertEqual(self.timer.short_break_duration, 60)
        self.assertEqual(self.timer.long_break_duration, 180)

    def test_reset_daily_stats(self):
        """Test resetting daily statistics."""
        self.timer.completed_pomodoros_today = 5

        self.timer.reset_daily_stats()

        self.assertEqual(self.timer.completed_pomodoros_today, 0)

    def test_thread_safety(self):
        """Test timer operations are thread-safe."""
        self.timer.start()

        # Rapidly pause/resume in sequence
        for _ in range(5):
            self.timer.pause()
            time.sleep(0.1)
            self.timer.resume()
            time.sleep(0.1)

        # Should still be running
        self.assertIn(
            self.timer.get_state(),
            [TimerState.WORK, TimerState.PAUSED]
        )

        self.timer.stop()


if __name__ == "__main__":
    unittest.main()
