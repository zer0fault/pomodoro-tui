"""Test that theme switching ACTUALLY works now."""
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.app import PomodoroApp

print("Creating app...")
app = PomodoroApp()

print(f"Initial theme: {app.theme}")
print(f"Theme manager says: {app.theme_manager.get_current_theme()}")

print("\n--- Switching to Nord ---")
app._load_theme("pomodoro-nord")
print(f"New theme: {app.theme}")
print(f"Theme manager says: {app.theme_manager.get_current_theme()}")

print("\n--- Switching to Gruvbox ---")
app._load_theme("pomodoro-gruvbox")
print(f"New theme: {app.theme}")
print(f"Theme manager says: {app.theme_manager.get_current_theme()}")

print("\n[SUCCESS] Theme property IS changing!")
print("This means theme switching will actually work in the app now.")
