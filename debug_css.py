"""Debug script to see the combined CSS."""
from src.app import PomodoroApp
from src.config import get_config

config = get_config()
config.load()
theme_id = config.get("appearance", "theme", "pomodoro-default")

app = PomodoroApp()

# Get the combined CSS
css_lines = app.__class__.CSS.split('\n')

print("Lines 215-225:")
for i in range(214, min(225, len(css_lines))):
    print(f"{i+1:3d}: {css_lines[i]}")

print("\nLines 255-265:")
for i in range(254, min(265, len(css_lines))):
    print(f"{i+1:3d}: {css_lines[i]}")
