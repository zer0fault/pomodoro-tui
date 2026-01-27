"""
Pomodoro timer logic implementation.
"""
import threading
import time
from typing import Callable, Optional, Dict, Any
from enum import Enum

from src.utils.constants import (
    STATE_IDLE,
    STATE_WORK,
    STATE_SHORT_BREAK,
    STATE_LONG_BREAK,
    STATE_PAUSED,
    DEFAULT_WORK_DURATION,
    DEFAULT_SHORT_BREAK_DURATION,
    DEFAULT_LONG_BREAK_DURATION,
    DEFAULT_POMODOROS_UNTIL_LONG_BREAK,
)
from src.utils.helpers import minutes_to_seconds, calculate_progress


class TimerState(Enum):
    """Enumeration of timer states."""
    IDLE = STATE_IDLE
    WORK = STATE_WORK
    SHORT_BREAK = STATE_SHORT_BREAK
    LONG_BREAK = STATE_LONG_BREAK
    PAUSED = STATE_PAUSED


class PomodoroTimer:
    """
    Core Pomodoro timer with state management and event callbacks.

    Implements the traditional Pomodoro technique with work sessions,
    short breaks, and long breaks after completing multiple pomodoros.
    """

    def __init__(
        self,
        work_duration: int = DEFAULT_WORK_DURATION,
        short_break_duration: int = DEFAULT_SHORT_BREAK_DURATION,
        long_break_duration: int = DEFAULT_LONG_BREAK_DURATION,
        pomodoros_until_long_break: int = DEFAULT_POMODOROS_UNTIL_LONG_BREAK,
    ):
        """
        Initialize the Pomodoro timer.

        Args:
            work_duration: Work session duration in minutes
            short_break_duration: Short break duration in minutes
            long_break_duration: Long break duration in minutes
            pomodoros_until_long_break: Number of pomodoros before long break
        """
        # Duration settings (in seconds)
        self.work_duration = minutes_to_seconds(work_duration)
        self.short_break_duration = minutes_to_seconds(short_break_duration)
        self.long_break_duration = minutes_to_seconds(long_break_duration)
        self.pomodoros_until_long_break = pomodoros_until_long_break

        # Timer state
        self.state = TimerState.IDLE
        self.previous_state: Optional[TimerState] = None

        # Time tracking
        self.total_seconds = 0
        self.elapsed_seconds = 0
        self.remaining_seconds = 0

        # Session tracking
        self.current_pomodoro = 0  # Current pomodoro in the cycle (0-indexed)
        self.completed_pomodoros_today = 0

        # Threading
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._running = False
        self._lock = threading.RLock()  # Use RLock for reentrant locking

        # Event callbacks
        self._callbacks: Dict[str, list[Callable]] = {
            "tick": [],
            "session_complete": [],
            "break_complete": [],
            "cycle_complete": [],
            "state_change": [],
        }

    def on(self, event: str, callback: Callable) -> None:
        """
        Register a callback for a timer event.

        Args:
            event: Event name (tick, session_complete, break_complete,
                   cycle_complete, state_change)
            callback: Callback function to invoke
        """
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def off(self, event: str, callback: Callable) -> None:
        """
        Unregister a callback for a timer event.

        Args:
            event: Event name
            callback: Callback function to remove
        """
        if event in self._callbacks and callback in self._callbacks[event]:
            self._callbacks[event].remove(callback)

    def _emit(self, event: str, *args, **kwargs) -> None:
        """
        Emit an event to all registered callbacks.

        Args:
            event: Event name
            *args: Positional arguments for callbacks
            **kwargs: Keyword arguments for callbacks
        """
        if event in self._callbacks:
            for callback in self._callbacks[event]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Error in callback for {event}: {e}")

    def _change_state(self, new_state: TimerState) -> None:
        """
        Change the timer state and emit state_change event.

        Args:
            new_state: New timer state
        """
        with self._lock:
            old_state = self.state
            self.state = new_state
            if old_state != new_state:
                self._emit("state_change", old_state, new_state)

    def start(self) -> bool:
        """
        Start a work session.

        Returns:
            True if started successfully, False otherwise
        """
        with self._lock:
            if self._running:
                return False

            # Start a new work session
            self._change_state(TimerState.WORK)
            self.total_seconds = self.work_duration
            self.elapsed_seconds = 0
            self.remaining_seconds = self.total_seconds

            # Start the timer thread
            self._running = True
            self._stop_event.clear()
            self._timer_thread = threading.Thread(target=self._run, daemon=True)
            self._timer_thread.start()

            return True

    def pause(self) -> bool:
        """
        Pause the current session.

        Returns:
            True if paused successfully, False otherwise
        """
        with self._lock:
            if not self._running or self.state == TimerState.IDLE:
                return False

            if self.state != TimerState.PAUSED:
                self.previous_state = self.state
                self._change_state(TimerState.PAUSED)
                return True

            return False

    def resume(self) -> bool:
        """
        Resume a paused session.

        Returns:
            True if resumed successfully, False otherwise
        """
        with self._lock:
            if not self._running or self.state != TimerState.PAUSED:
                return False

            if self.previous_state:
                self._change_state(self.previous_state)
                self.previous_state = None
                return True

            return False

    def stop(self) -> bool:
        """
        Stop the timer and reset to idle state.

        Returns:
            True if stopped successfully, False otherwise
        """
        with self._lock:
            if not self._running:
                return False

            self._running = False
            self._stop_event.set()

        # Wait for thread to finish
        if self._timer_thread and self._timer_thread.is_alive():
            self._timer_thread.join(timeout=2)

        with self._lock:
            self._change_state(TimerState.IDLE)
            self.elapsed_seconds = 0
            self.remaining_seconds = 0
            self.total_seconds = 0

            return True

    def skip(self) -> bool:
        """
        Skip to the next phase (complete current session early).

        Returns:
            True if skipped successfully, False otherwise
        """
        with self._lock:
            if not self._running or self.state in [TimerState.IDLE, TimerState.PAUSED]:
                return False

            # Force completion of current session
            self.elapsed_seconds = self.total_seconds
            self.remaining_seconds = 0

            return True

    def _run(self) -> None:
        """Main timer loop running in separate thread."""
        while self._running and not self._stop_event.is_set():
            # Wait for 1 second or until stop event
            if self._stop_event.wait(1.0):
                break

            with self._lock:
                # Only count down if not paused
                if self.state != TimerState.PAUSED:
                    self.elapsed_seconds += 1
                    self.remaining_seconds = self.total_seconds - self.elapsed_seconds

                    # Emit tick event
                    self._emit("tick", self.remaining_seconds)

                    # Check if session is complete
                    if self.remaining_seconds <= 0:
                        self._handle_session_complete()

    def _handle_session_complete(self) -> None:
        """Handle completion of a timer session (work or break)."""
        current_state = self.state

        if current_state == TimerState.WORK:
            # Work session completed
            self.current_pomodoro += 1
            self.completed_pomodoros_today += 1
            self._emit("session_complete", self.current_pomodoro)

            # Determine next break type
            if self.current_pomodoro >= self.pomodoros_until_long_break:
                # Time for long break
                self._start_break(TimerState.LONG_BREAK)
                self._emit("cycle_complete", self.current_pomodoro)
                self.current_pomodoro = 0  # Reset cycle
            else:
                # Short break
                self._start_break(TimerState.SHORT_BREAK)

        elif current_state in [TimerState.SHORT_BREAK, TimerState.LONG_BREAK]:
            # Break completed
            self._emit("break_complete", current_state)

            # Automatically transition back to idle
            # (User will manually start next work session)
            self._running = False
            self._change_state(TimerState.IDLE)

    def _start_break(self, break_type: TimerState) -> None:
        """
        Start a break session.

        Args:
            break_type: Type of break (SHORT_BREAK or LONG_BREAK)
        """
        self._change_state(break_type)

        if break_type == TimerState.SHORT_BREAK:
            self.total_seconds = self.short_break_duration
        else:
            self.total_seconds = self.long_break_duration

        self.elapsed_seconds = 0
        self.remaining_seconds = self.total_seconds

    def get_remaining_time(self) -> int:
        """
        Get remaining time in current session.

        Returns:
            Remaining seconds
        """
        with self._lock:
            return self.remaining_seconds

    def get_elapsed_time(self) -> int:
        """
        Get elapsed time in current session.

        Returns:
            Elapsed seconds
        """
        with self._lock:
            return self.elapsed_seconds

    def get_progress(self) -> float:
        """
        Get progress of current session.

        Returns:
            Progress as float between 0.0 and 1.0
        """
        with self._lock:
            return calculate_progress(self.elapsed_seconds, self.total_seconds)

    def get_state(self) -> TimerState:
        """
        Get current timer state.

        Returns:
            Current TimerState
        """
        with self._lock:
            return self.state

    def get_session_info(self) -> Dict[str, Any]:
        """
        Get current session information.

        Returns:
            Dictionary with session details
        """
        with self._lock:
            return {
                "state": self.state.value,
                "current_pomodoro": self.current_pomodoro,
                "pomodoros_until_long_break": self.pomodoros_until_long_break,
                "completed_today": self.completed_pomodoros_today,
                "remaining_seconds": self.remaining_seconds,
                "elapsed_seconds": self.elapsed_seconds,
                "total_seconds": self.total_seconds,
                "progress": calculate_progress(self.elapsed_seconds, self.total_seconds),
            }

    def update_durations(
        self,
        work_duration: Optional[int] = None,
        short_break_duration: Optional[int] = None,
        long_break_duration: Optional[int] = None,
        pomodoros_until_long_break: Optional[int] = None,
    ) -> None:
        """
        Update timer duration settings.

        Args:
            work_duration: Work session duration in minutes
            short_break_duration: Short break duration in minutes
            long_break_duration: Long break duration in minutes
            pomodoros_until_long_break: Number of pomodoros before long break
        """
        with self._lock:
            if work_duration is not None:
                self.work_duration = minutes_to_seconds(work_duration)
            if short_break_duration is not None:
                self.short_break_duration = minutes_to_seconds(short_break_duration)
            if long_break_duration is not None:
                self.long_break_duration = minutes_to_seconds(long_break_duration)
            if pomodoros_until_long_break is not None:
                self.pomodoros_until_long_break = pomodoros_until_long_break

    def reset_daily_stats(self) -> None:
        """Reset daily statistics (call at start of new day)."""
        with self._lock:
            self.completed_pomodoros_today = 0
