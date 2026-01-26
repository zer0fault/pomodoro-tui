#!/usr/bin/env python
"""
Pomodoro TUI - An aesthetic terminal Pomodoro timer application.

Entry point for the application.
"""
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.app import run


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
