"""
Timer display widget showing countdown and current phase.
"""
from textual.app import ComposeResult
from textual.widgets import Static
from textual.reactive import reactive

from src.utils.helpers import format_time
from src.utils.constants import (
    STATE_IDLE,
    STATE_WORK,
    STATE_SHORT_BREAK,
    STATE_LONG_BREAK,
    STATE_PAUSED,
    PHASE_NAMES,
    CSS_CLASS_TIMER_WORK,
    CSS_CLASS_TIMER_BREAK,
    CSS_CLASS_TIMER_IDLE,
    CSS_CLASS_TIMER_PAUSED,
)


class TimerDisplay(Static):
    """
    Large timer display widget showing time and current phase.

    Shows countdown in MM:SS format with phase indicator.
    Color-coded based on current timer state.
    """

    # Reactive properties for automatic UI updates
    time_remaining = reactive(0)
    current_phase = reactive(STATE_IDLE)

    def __init__(self, *args, **kwargs):
        """Initialize the timer display."""
        super().__init__(*args, **kwargs)
        self.border_title = "Pomodoro Timer"

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static(id="timer-time")
        yield Static(id="timer-phase")

    def on_mount(self) -> None:
        """Called when widget is mounted."""
        self.update_display()

    def watch_time_remaining(self, new_time: int) -> None:
        """Called when time_remaining changes."""
        self.update_display()

    def watch_current_phase(self, new_phase: str) -> None:
        """Called when current_phase changes."""
        self.update_display()
        self.update_styling()

    def update_display(self) -> None:
        """Update the displayed time and phase."""
        # Update time display
        time_widget = self.query_one("#timer-time", Static)
        time_str = format_time(self.time_remaining)
        time_widget.update(f"[bold]{time_str}[/bold]")

        # Update phase display
        phase_widget = self.query_one("#timer-phase", Static)
        phase_name = PHASE_NAMES.get(self.current_phase, "READY")
        phase_widget.update(f"[italic]{phase_name}[/italic]")

    def update_styling(self) -> None:
        """Update CSS classes based on current phase."""
        # Remove all phase classes
        self.remove_class(CSS_CLASS_TIMER_WORK)
        self.remove_class(CSS_CLASS_TIMER_BREAK)
        self.remove_class(CSS_CLASS_TIMER_IDLE)
        self.remove_class(CSS_CLASS_TIMER_PAUSED)

        # Add appropriate class for current phase
        if self.current_phase == STATE_WORK:
            self.add_class(CSS_CLASS_TIMER_WORK)
        elif self.current_phase in [STATE_SHORT_BREAK, STATE_LONG_BREAK]:
            self.add_class(CSS_CLASS_TIMER_BREAK)
        elif self.current_phase == STATE_PAUSED:
            self.add_class(CSS_CLASS_TIMER_PAUSED)
        else:
            self.add_class(CSS_CLASS_TIMER_IDLE)

    def set_time(self, seconds: int) -> None:
        """
        Set the displayed time.

        Args:
            seconds: Time to display in seconds
        """
        self.time_remaining = seconds

    def set_phase(self, phase: str) -> None:
        """
        Set the current phase.

        Args:
            phase: Phase name (IDLE, WORK, SHORT_BREAK, etc.)
        """
        self.current_phase = phase
