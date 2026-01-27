"""
Test that the app can start and load themes without errors.
"""
import sys
import io

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.app import PomodoroApp
from src.config import get_config


def test_app_creation():
    """Test that we can create the app instance."""
    print("Testing app creation...")
    try:
        app = PomodoroApp()
        print("[OK] App created successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to create app: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_theme_loading():
    """Test that theme loading works."""
    print("\nTesting theme loading...")
    try:
        app = PomodoroApp()

        # Test loading default theme
        app._load_theme("pomodoro-default")
        print("[OK] Default theme loaded")

        # Test loading Catppuccin theme
        app._load_theme("pomodoro-catppuccin")
        print("[OK] Catppuccin theme loaded")

        # Test loading Nord theme
        app._load_theme("pomodoro-nord")
        print("[OK] Nord theme loaded")

        return True
    except Exception as e:
        print(f"[FAIL] Failed to load themes: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_loading():
    """Test that config loads properly."""
    print("\nTesting config loading...")
    try:
        config = get_config()
        config.load()
        theme = config.get("appearance", "theme", "pomodoro-default")
        print(f"[OK] Config loaded, theme setting: {theme}")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to load config: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("App Startup Tests")
    print("=" * 60)

    all_passed = True

    all_passed &= test_config_loading()
    all_passed &= test_app_creation()
    all_passed &= test_theme_loading()

    print("\n" + "=" * 60)
    if all_passed:
        print("[PASS] All tests PASSED - App should start successfully!")
        print("=" * 60)
        print("\nYou can now run: python main.py")
        sys.exit(0)
    else:
        print("[FAIL] Some tests FAILED")
        print("=" * 60)
        sys.exit(1)
