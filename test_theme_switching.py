"""
Quick test to verify theme switching works.
"""
import sys
import io

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.app import PomodoroApp


def test_theme_switching():
    """Test that themes can be switched."""
    print("Testing theme switching...")
    try:
        app = PomodoroApp()

        # Check initial theme loaded
        initial_theme = app.theme_manager.get_current_theme()
        print(f"[OK] Initial theme: {initial_theme}")

        # Test switching to different themes
        themes_to_test = ["pomodoro-catppuccin", "pomodoro-nord", "pomodoro-gruvbox"]

        for theme_id in themes_to_test:
            app._load_theme(theme_id)
            current = app.theme_manager.get_current_theme()
            if current == theme_id:
                print(f"[OK] Switched to {theme_id}")
            else:
                print(f"[FAIL] Theme not switched: expected {theme_id}, got {current}")
                return False

        print("[PASS] Theme switching works!")
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Theme Switching Test")
    print("=" * 60)
    print()

    if test_theme_switching():
        print("\n" + "=" * 60)
        print("[SUCCESS] Ready to test in the app!")
        print("=" * 60)
        print("\nRun: python main.py")
        print("Then press T to open theme picker")
        print("Use arrow keys to navigate, Enter to apply")
        sys.exit(0)
    else:
        sys.exit(1)
