"""
Main Textual application for the Pomodoro TUI.
"""
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Center
from textual.widgets import Header, Footer, Static, Button
from textual.binding import Binding

from src.config import get_config
from src.timer import PomodoroTimer, TimerState
from src.components.timer_display import TimerDisplay
from src.components.progress_bar import PomodoroProgressBar
from src.components.theme_picker import ThemePicker
from src.theme_manager import get_theme_manager
from src.utils.constants import (
    APP_NAME,
    STATE_IDLE,
    STATE_WORK,
    STATE_PAUSED,
)


class SessionCounter(Static):
    """Widget displaying current session count."""

    def __init__(self, *args, **kwargs):
        """Initialize session counter."""
        super().__init__(*args, **kwargs)
        self.current = 0
        self.total = 4

    def update_count(self, current: int, total: int) -> None:
        """
        Update the session counter display.

        Args:
            current: Current pomodoro number
            total: Total pomodoros until long break
        """
        self.current = current
        self.total = total
        if current == 0:
            self.update("[dim]Ready to begin[/dim]")
        else:
            self.update(f"[bold]Session {current} of {total}[/bold] before long break")


class PomodoroApp(App):
    """Main Pomodoro TUI application."""

    # Base CSS for layout structure
    CSS = """
    Screen {
        align: center middle;
    }

    #main-container {
        width: 80;
        height: auto;
        padding: 1 2;
    }

    TimerDisplay {
        width: 100%;
        height: auto;
        padding: 2 4;
        text-align: center;
        margin-bottom: 1;
    }

    #timer-time {
        text-style: bold;
        text-align: center;
        content-align: center middle;
        height: 3;
        width: 100%;
    }

    #timer-phase {
        text-style: italic;
        text-align: center;
        content-align: center middle;
        height: 1;
        width: 100%;
        margin-top: 1;
    }

    PomodoroProgressBar {
        width: 100%;
        margin: 1 0;
        height: 1;
    }

    PomodoroProgressBar > .bar--bar {
        color: $success;
    }

    PomodoroProgressBar > .bar--complete {
        color: $success-darken-1;
    }

    PomodoroProgressBar.work > .bar--bar {
        color: $error;
    }

    PomodoroProgressBar.work > .bar--complete {
        color: $error-darken-1;
    }

    PomodoroProgressBar.break > .bar--bar {
        color: $success;
    }

    PomodoroProgressBar.break > .bar--complete {
        color: $success-darken-1;
    }

    SessionCounter {
        width: 100%;
        text-align: center;
        margin: 1 0;
    }

    #control-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;
    }

    Button {
        margin: 0 1;
        min-width: 10;
    }

    #help-text {
        width: 100%;
        text-align: center;
        margin-top: 2;
    }
    """

    BINDINGS = [
        Binding("space", "toggle_timer", "Start/Pause", priority=True),
        Binding("s", "stop_timer", "Stop"),
        Binding("n", "skip_phase", "Skip"),
        Binding("t", "toggle_theme_picker", "Theme", priority=True),
        Binding("q", "quit", "Quit", priority=True),
        Binding("question_mark", "help", "Help"),
        Binding("c", "config", "Settings"),
    ]

    TITLE = APP_NAME

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.config = get_config()
        self.theme_manager = get_theme_manager()
        self._initial_theme_loaded = False

        # Initialize timer with config values
        work_duration = self.config.get("timer", "work_duration", 25)
        short_break = self.config.get("timer", "short_break_duration", 5)
        long_break = self.config.get("timer", "long_break_duration", 15)
        pomodoros_until_long = self.config.get("timer", "pomodoros_until_long_break", 4)

        self.timer = PomodoroTimer(
            work_duration=work_duration,
            short_break_duration=short_break,
            long_break_duration=long_break,
            pomodoros_until_long_break=pomodoros_until_long,
        )

        # Register timer callbacks
        self.timer.on("tick", self._on_timer_tick)
        self.timer.on("state_change", self._on_state_change)
        self.timer.on("session_complete", self._on_session_complete)
        self.timer.on("break_complete", self._on_break_complete)
        self.timer.on("cycle_complete", self._on_cycle_complete)

        # Map our theme IDs to Textual's built-in themes
        self.theme_map = {
            "pomodoro-default": "textual-dark",  # Use dark as default purple
            "pomodoro-catppuccin": "catppuccin-mocha",
            "pomodoro-nord": "nord",
            "pomodoro-gruvbox": "gruvbox",
            "pomodoro-tokyo-night": "tokyo-night",
        }

        # Load initial theme using Textual's built-in system
        theme_id = self.config.get("appearance", "theme", "pomodoro-default")
        textual_theme = self.theme_map.get(theme_id, "textual-dark")
        self.theme = textual_theme
        self.theme_manager.set_current_theme(theme_id)
        self._initial_theme_loaded = True

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            TimerDisplay(id="timer-display"),
            PomodoroProgressBar(id="progress-bar"),
            SessionCounter(id="session-counter"),
            Horizontal(
                Button("Start", id="btn-start", variant="success"),
                Button("Pause", id="btn-pause", variant="primary"),
                Button("Stop", id="btn-stop", variant="error"),
                Button("Skip", id="btn-skip", variant="default"),
                id="control-buttons",
            ),
            Static(
                "[dim]Space[/dim] Start/Pause  •  [dim]S[/dim] Stop  •  "
                "[dim]N[/dim] Skip  •  [dim]T[/dim] Theme  •  [dim]Q[/dim] Quit",
                id="help-text"
            ),
            id="main-container"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        # Load configuration
        self.config.load()

        # Initialize display
        self._update_timer_display()
        self._update_session_counter()
        self._update_buttons()

    def _update_timer_display(self) -> None:
        """Update the timer display with current time and phase."""
        timer_display = self.query_one("#timer-display", TimerDisplay)
        timer_display.set_time(self.timer.get_remaining_time())
        timer_display.set_phase(self.timer.get_state().value)

    def _update_progress_bar(self) -> None:
        """Update the progress bar."""
        progress_bar = self.query_one("#progress-bar", PomodoroProgressBar)
        progress = self.timer.get_progress()
        progress_bar.set_progress(progress)
        progress_bar.set_phase(self.timer.get_state().value)

    def _update_session_counter(self) -> None:
        """Update the session counter."""
        session_counter = self.query_one("#session-counter", SessionCounter)
        info = self.timer.get_session_info()
        session_counter.update_count(
            info["current_pomodoro"],
            info["pomodoros_until_long_break"]
        )

    def _update_buttons(self) -> None:
        """Update button states based on timer state."""
        state = self.timer.get_state()

        try:
            btn_start = self.query_one("#btn-start", Button)
            btn_pause = self.query_one("#btn-pause", Button)
            btn_stop = self.query_one("#btn-stop", Button)
            btn_skip = self.query_one("#btn-skip", Button)

            if state == TimerState.IDLE:
                btn_start.disabled = False
                btn_pause.disabled = True
                btn_stop.disabled = True
                btn_skip.disabled = True
            elif state == TimerState.PAUSED:
                btn_start.disabled = False  # Can resume
                btn_pause.disabled = True
                btn_stop.disabled = False
                btn_skip.disabled = False
            else:  # WORK, SHORT_BREAK, LONG_BREAK
                btn_start.disabled = True
                btn_pause.disabled = False
                btn_stop.disabled = False
                btn_skip.disabled = False
        except Exception:
            # Buttons might not be mounted yet
            pass

    # Timer callback methods
    def _on_timer_tick(self, remaining_seconds: int) -> None:
        """Called every second when timer ticks."""
        # Only update if not paused (should not receive ticks when paused, but double-check)
        if self.timer.get_state() != TimerState.PAUSED:
            self._update_timer_display()
            self._update_progress_bar()

    def _on_state_change(self, old_state: TimerState, new_state: TimerState) -> None:
        """Called when timer state changes."""
        self._update_timer_display()
        self._update_buttons()

        # Show notification for state changes
        if new_state == TimerState.WORK:
            self.notify("🍅 Focus time! Let's get to work.", severity="information")
        elif new_state.value in ["SHORT_BREAK", "LONG_BREAK"]:
            break_type = "short" if new_state.value == "SHORT_BREAK" else "long"
            self.notify(f"☕ Time for a {break_type} break!", severity="information")

    def _on_session_complete(self, pomodoro_num: int) -> None:
        """Called when a work session completes."""
        self.notify(
            f"✅ Pomodoro #{pomodoro_num} completed!",
            severity="information",
            timeout=5
        )
        self._update_session_counter()

    def _on_break_complete(self, break_type: TimerState) -> None:
        """Called when a break completes."""
        self.notify("✨ Break finished! Ready for another session?", severity="information")
        self._update_timer_display()

    def _on_cycle_complete(self, pomodoro_num: int) -> None:
        """Called when a full cycle completes."""
        self.notify(
            f"🎉 Cycle complete! {pomodoro_num} pomodoros done. Long break time!",
            severity="information",
            timeout=5
        )

    # Action methods for keyboard bindings
    def action_toggle_timer(self) -> None:
        """Toggle timer between start/pause."""
        state = self.timer.get_state()

        if state == TimerState.IDLE:
            # Start new work session
            self.timer.start()
        elif state == TimerState.PAUSED:
            # Resume
            self.timer.resume()
        elif state in [TimerState.WORK, TimerState.SHORT_BREAK, TimerState.LONG_BREAK]:
            # Pause
            self.timer.pause()

    def action_stop_timer(self) -> None:
        """Stop the timer and reset."""
        if self.timer.get_state() != TimerState.IDLE:
            self.timer.stop()
            self._update_timer_display()
            self._update_progress_bar()
            self._update_session_counter()
            self.notify("Timer stopped", severity="warning")

    def action_skip_phase(self) -> None:
        """Skip to next phase."""
        if self.timer.get_state() not in [TimerState.IDLE, TimerState.PAUSED]:
            self.timer.skip()
            self.notify("Skipped to next phase", severity="information")

    def action_help(self) -> None:
        """Show help screen."""
        self.notify("Help screen coming in Phase 9!", severity="information")

    def action_config(self) -> None:
        """Open configuration/settings."""
        self.notify("Settings panel coming in Phase 6!", severity="information")

    def action_quit(self) -> None:
        """Quit the application."""
        # Stop timer before exiting
        if self.timer.get_state() != TimerState.IDLE:
            self.timer.stop()
        self.exit()

    # Theme management methods
    def _load_theme(self, theme_id: str) -> None:
        """
        Load and apply a theme dynamically using Textual's built-in theme system.

        Args:
            theme_id: ID of the theme to load
        """
        try:
            # Map to Textual's built-in theme
            textual_theme = self.theme_map.get(theme_id)
            if not textual_theme:
                self.notify(f"Theme not found: {theme_id}", severity="error")
                return

            # Use Textual's native theme switching - this actually works!
            self.theme = textual_theme

            # Update theme manager state
            self.theme_manager.set_current_theme(theme_id)

            # Save to config
            self.config.set("appearance", "theme", theme_id)
            self.config.save()

            # Show notification
            self.notify(
                f"Theme: {self.theme_manager.get_current_theme_name()}",
                severity="information",
                timeout=2
            )
        except Exception as e:
            self.notify(f"Error loading theme: {e}", severity="error")
            import traceback
            traceback.print_exc()

    def _switch_theme(self, theme_id: str) -> None:
        """
        Switch to a new theme and save to config.

        Args:
            theme_id: ID of the theme to switch to
        """
        self._load_theme(theme_id)

    def action_toggle_theme_picker(self) -> None:
        """Open the theme picker."""
        def handle_theme_selection(selected_theme: str | None) -> None:
            """Handle theme selection from picker."""
            if selected_theme:
                self._switch_theme(selected_theme)

        self.push_screen(ThemePicker(), handle_theme_selection)

    # Button event handlers
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id

        if button_id == "btn-start":
            if self.timer.get_state() == TimerState.IDLE:
                self.timer.start()
            elif self.timer.get_state() == TimerState.PAUSED:
                self.timer.resume()
        elif button_id == "btn-pause":
            self.timer.pause()
        elif button_id == "btn-stop":
            self.action_stop_timer()
        elif button_id == "btn-skip":
            self.action_skip_phase()


def run() -> None:
    """Run the Pomodoro TUI application."""
    app = PomodoroApp()
    app.run()


if __name__ == "__main__":
    run()
