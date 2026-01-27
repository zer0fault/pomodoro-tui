"""
Quick integration test for Phase 4 theming system.
Tests theme loading, switching, and persistence.
"""
import sys
import io

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.theme_manager import get_theme_manager
from src.config import get_config


def test_theme_manager():
    """Test theme manager functionality."""
    print("=" * 60)
    print("Testing Theme Manager")
    print("=" * 60)

    tm = get_theme_manager()

    # Test 1: Get available themes
    themes = tm.get_available_themes()
    print(f"\n[OK] Found {len(themes)} themes:")
    for theme_id, name in themes.items():
        print(f"  - {name} ({theme_id})")

    assert len(themes) == 5, "Expected 5 themes"
    assert "pomodoro-default" in themes
    assert "pomodoro-catppuccin" in themes
    assert "pomodoro-nord" in themes
    assert "pomodoro-gruvbox" in themes
    assert "pomodoro-tokyo-night" in themes

    # Test 2: Load each theme
    print("\n[OK] Theme loading:")
    for theme_id in themes.keys():
        css = tm.load_theme(theme_id)
        assert css is not None, f"Failed to load {theme_id}"
        assert len(css) > 0, f"{theme_id} is empty"
        print(f"  - {themes[theme_id]}: {len(css)} characters")

    # Test 3: Set current theme
    print("\n[OK] Theme switching:")
    for theme_id in themes.keys():
        result = tm.set_current_theme(theme_id)
        assert result, f"Failed to set {theme_id}"
        assert tm.get_current_theme() == theme_id
        print(f"  - Switched to {themes[theme_id]}")

    # Test 4: Theme cycling
    print("\n[OK] Theme cycling:")
    tm.set_current_theme("pomodoro-default")
    next_theme = tm.get_next_theme()
    assert next_theme == "pomodoro-catppuccin", "Next theme should be catppuccin"
    print(f"  - Next: {next_theme}")

    prev_theme = tm.get_previous_theme()
    assert prev_theme == "pomodoro-tokyo-night", "Previous should wrap to last theme"
    print(f"  - Previous: {prev_theme}")

    print("\n[PASS] Theme Manager: All tests passed!")


def test_config_persistence():
    """Test theme persistence in config."""
    print("\n" + "=" * 60)
    print("Testing Config Persistence")
    print("=" * 60)

    cfg = get_config()
    cfg.load()

    # Test saving different themes
    test_themes = ["pomodoro-catppuccin", "pomodoro-nord", "pomodoro-default"]

    for theme_id in test_themes:
        cfg.set("appearance", "theme", theme_id)
        cfg.save()

        # Reload config
        cfg.load()
        saved_theme = cfg.get("appearance", "theme", "pomodoro-default")
        assert saved_theme == theme_id, f"Theme not persisted: expected {theme_id}, got {saved_theme}"
        print(f"  [OK] Theme persisted: {theme_id}")

    # Reset to default
    cfg.set("appearance", "theme", "pomodoro-default")
    cfg.save()

    print("\n[PASS] Config Persistence: All tests passed!")


def test_theme_file_content():
    """Verify theme files have proper structure."""
    print("\n" + "=" * 60)
    print("Testing Theme File Content")
    print("=" * 60)

    tm = get_theme_manager()
    themes = tm.get_available_themes()

    required_elements = [
        "Screen {",
        "Header {",
        "Footer {",
        "Button {",
        "TimerDisplay {",
        "$primary:",
        "$text:",
    ]

    for theme_id, theme_name in themes.items():
        css = tm.load_theme(theme_id)
        print(f"\n  Checking {theme_name}:")

        for element in required_elements:
            if element in css:
                print(f"    [OK] {element}")
            else:
                print(f"    [FAIL] Missing: {element}")
                assert False, f"{theme_id} missing {element}"

    print("\n[PASS] Theme File Content: All tests passed!")


if __name__ == "__main__":
    try:
        test_theme_manager()
        test_config_persistence()
        test_theme_file_content()

        print("\n" + "=" * 60)
        print("[SUCCESS] Phase 4 Integration Tests: ALL PASSED")
        print("=" * 60)
        print("\nPhase 4 (Theming System) is complete and ready!")

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
