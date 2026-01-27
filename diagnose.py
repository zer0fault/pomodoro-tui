#!/usr/bin/env python
"""
Diagnostic script to check what's happening with the app.
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("="*60)
print("DIAGNOSTIC CHECKS")
print("="*60)

# Test 1: Import
print("\n1. Testing imports...")
try:
    from src.app import PomodoroApp
    from src.timer import PomodoroTimer
    from src.components.timer_display import TimerDisplay
    print("   ✓ All imports successful")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Create timer
print("\n2. Testing timer creation...")
try:
    timer = PomodoroTimer(work_duration=1)
    print(f"   ✓ Timer created, state: {timer.get_state()}")
except Exception as e:
    print(f"   ✗ Timer creation failed: {e}")
    sys.exit(1)

# Test 3: Timer start
print("\n3. Testing timer start...")
try:
    result = timer.start()
    print(f"   ✓ Timer start result: {result}")
    print(f"   ✓ Timer state: {timer.get_state()}")
    print(f"   ✓ Remaining: {timer.get_remaining_time()}s")
    timer.stop()
except Exception as e:
    print(f"   ✗ Timer start failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Create app
print("\n4. Testing app creation...")
try:
    app = PomodoroApp()
    print(f"   ✓ App created")
    print(f"   ✓ App title: {app.TITLE}")
    print(f"   ✓ Timer state: {app.timer.get_state()}")
except Exception as e:
    print(f"   ✗ App creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Check bindings
print("\n5. Checking key bindings...")
try:
    bindings = app.BINDINGS
    print(f"   ✓ Found {len(bindings)} bindings:")
    for binding in bindings:
        print(f"      - {binding.key} -> {binding.action} ({binding.description})")
except Exception as e:
    print(f"   ✗ Binding check failed: {e}")

# Test 6: Test action method directly
print("\n6. Testing action_toggle_timer directly...")
try:
    initial_state = app.timer.get_state()
    print(f"   Initial state: {initial_state}")

    app.action_toggle_timer()

    after_state = app.timer.get_state()
    print(f"   After toggle state: {after_state}")
    print(f"   Remaining: {app.timer.get_remaining_time()}s")

    if initial_state != after_state:
        print("   ✓ Action method works!")
    else:
        print("   ✗ State didn't change")

    app.timer.stop()
except Exception as e:
    print(f"   ✗ Action test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
print("\nIf all tests passed, the issue is with input/event handling.")
print("Try running: python test_minimal.py")
print("="*60)
