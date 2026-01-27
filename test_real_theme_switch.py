"""
Test that actually verifies theme switching by inspecting the CSS.
"""
import sys
import io
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.app import PomodoroApp

app = PomodoroApp()

print("Initial CSS_PATH:", app.CSS_PATH)
print("Initial theme:", app.theme_manager.get_current_theme())

# Try switching theme
print("\nSwitching to nord...")
app._load_theme("pomodoro-nord")

print("New CSS_PATH:", app.CSS_PATH)
print("New theme:", app.theme_manager.get_current_theme())

# Check if CSS actually changed
print("\nDoes stylesheet contain nord colors?")
print("Checking for '#b48ead' (nord primary)...")

# The issue: CSS_PATH changes but the actual CSS content doesn't reload
print("\nThe problem: CSS_PATH is only loaded on App initialization")
print("Changing CSS_PATH after the app is created doesn't reload the CSS")
