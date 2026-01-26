"""
Constants and default values for the Pomodoro TUI application.
"""

# Application metadata
APP_NAME = "Pomodoro TUI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "An aesthetic terminal Pomodoro timer"

# Timer states
STATE_IDLE = "IDLE"
STATE_WORK = "WORK"
STATE_SHORT_BREAK = "SHORT_BREAK"
STATE_LONG_BREAK = "LONG_BREAK"
STATE_PAUSED = "PAUSED"

# Default timer durations (in minutes)
DEFAULT_WORK_DURATION = 25
DEFAULT_SHORT_BREAK_DURATION = 5
DEFAULT_LONG_BREAK_DURATION = 15
DEFAULT_POMODOROS_UNTIL_LONG_BREAK = 4

# Timer duration limits (in minutes)
MIN_WORK_DURATION = 15
MAX_WORK_DURATION = 45
MIN_SHORT_BREAK_DURATION = 3
MAX_SHORT_BREAK_DURATION = 10
MIN_LONG_BREAK_DURATION = 10
MAX_LONG_BREAK_DURATION = 30
MIN_POMODOROS_UNTIL_LONG_BREAK = 2
MAX_POMODOROS_UNTIL_LONG_BREAK = 6

# Phase display names
PHASE_NAMES = {
    STATE_WORK: "FOCUS TIME",
    STATE_SHORT_BREAK: "SHORT BREAK",
    STATE_LONG_BREAK: "LONG BREAK",
    STATE_IDLE: "READY",
    STATE_PAUSED: "PAUSED"
}

# Configuration paths
CONFIG_DIR = "~/.pomodoro-tui"
CONFIG_FILE = "config.toml"
HISTORY_FILE = "history.json"

# Default theme
DEFAULT_THEME = "pomodoro-default"

# ASCII art styles
ART_STYLE_TOMATO = "tomato"
ART_STYLE_MINIMAL = "minimal"
ART_STYLE_FANCY = "fancy"

# Audio defaults
DEFAULT_VOLUME = 0.7
DEFAULT_AUDIO_ENABLED = True

# UI update interval (seconds)
TIMER_TICK_INTERVAL = 1.0

# Color CSS classes
CSS_CLASS_TIMER_WORK = "timer-work"
CSS_CLASS_TIMER_BREAK = "timer-break"
CSS_CLASS_TIMER_IDLE = "timer-idle"
CSS_CLASS_TIMER_PAUSED = "timer-paused"
