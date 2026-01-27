#!/usr/bin/env python
"""
Debug version of app with logging to diagnose Space key issue.
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.app import PomodoroApp

# Patch the action_toggle_timer method to add logging
original_toggle = PomodoroApp.action_toggle_timer

def debug_toggle_timer(self):
    """Debug version with logging."""
    print(f"\n[DEBUG] action_toggle_timer called!")
    print(f"[DEBUG] Current timer state: {self.timer.get_state()}")
    result = original_toggle(self)
    print(f"[DEBUG] After toggle, state: {self.timer.get_state()}")
    print(f"[DEBUG] Remaining: {self.timer.get_remaining_time()}s\n")
    return result

PomodoroApp.action_toggle_timer = debug_toggle_timer

if __name__ == "__main__":
    print("="*50)
    print("DEBUG APP - Watch for [DEBUG] messages")
    print("Press Space to start timer")
    print("="*50)
    app = PomodoroApp()
    app.run()
