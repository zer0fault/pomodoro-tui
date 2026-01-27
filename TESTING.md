# Testing Guide

## Running Tests

### Unit Tests

Run all timer unit tests:
```bash
cd pomodoro-tui
venv\Scripts\activate
python -m unittest tests.test_timer -v
```

Run UI integration tests:
```bash
python -m unittest tests.test_ui_integration -v
```

Run all tests:
```bash
python -m unittest discover tests -v
```

## Manual Testing

### Test Space Key Functionality

Run the debug version of the app:
```bash
python debug_app.py
```

This version logs when the Space key action is triggered.

Expected behavior:
1. App shows "25:00" and "READY"
2. Press Space
3. Timer should change to "FOCUS TIME"
4. Countdown should start decreasing every second
5. Progress bar should fill

### Test Timer Controls

1. **Start**: Press Space when timer is idle
2. **Pause**: Press Space again while running
3. **Resume**: Press Space while paused
4. **Stop**: Press S to stop and reset
5. **Skip**: Press N to skip to next phase

### Test Full Cycle

1. Start timer (Space)
2. Let it run for a few seconds
3. Skip (N) to complete work session
4. Should auto-transition to short break
5. Skip break
6. Should return to idle

## Troubleshooting

### Space Key Not Working

If Space doesn't start the timer:

1. Check you're in the main app window (not terminal prompt)
2. Try clicking the "Start" button instead
3. Run `debug_app.py` to see debug logging
4. Check for Python errors in terminal

### Timer Not Counting Down

If timer starts but doesn't update:

1. Check terminal for errors
2. Verify threading is working (timer runs in background thread)
3. Check if display update callbacks are registered

##Test Coverage

Current test files:
- `tests/test_timer.py` - Timer logic tests (16 tests)
- `tests/test_ui_integration.py` - UI component tests (9 tests)

Total: 25+ automated tests
