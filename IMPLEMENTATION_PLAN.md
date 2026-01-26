# Pomodoro TUI - Implementation Plan

## Project Overview

**Name:** Pomodoro TUI
**Description:** An aesthetic terminal user interface (TUI) Pomodoro timer application for Windows, featuring customizable themes, ASCII art, and rich visual effects.

**Technology Stack:**
- **Language:** Python 3.11+
- **TUI Framework:** Textual (with Rich)
- **Audio:** winsound (Windows native) / playsound (fallback)
- **Configuration:** TOML for user preferences
- **Package Management:** pip / venv

**Key Features:**
- Traditional Pomodoro timer (25-5-15 minute cycles)
- Adjustable time settings (while respecting Pomodoro methodology)
- Multiple aesthetic themes (purple default, catppuccin, nord, gruvbox, tokyo-night, custom)
- ASCII art displays and box-drawing decorations
- Rich visual effects (progress bars, animations, color gradients)
- Audio notifications
- Session tracking and statistics
- Keyboard shortcuts for control
- Theme switcher with live preview

---

## Architecture

### Project Structure

```
pomodoro-tui/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata (optional)
├── README.md                   # User documentation
├── IMPLEMENTATION_PLAN.md      # This file
│
├── src/
│   ├── __init__.py
│   ├── app.py                  # Main Textual application class
│   ├── config.py               # Configuration management
│   ├── timer.py                # Pomodoro timer logic
│   ├── stats.py                # Session statistics tracking
│   ├── audio.py                # Sound notification handling
│   │
│   ├── components/             # UI components
│   │   ├── __init__.py
│   │   ├── timer_display.py   # Main timer widget
│   │   ├── progress_bar.py    # Custom progress bar
│   │   ├── settings_panel.py  # Settings modal/screen
│   │   ├── stats_panel.py     # Statistics display
│   │   ├── theme_picker.py    # Theme selection widget
│   │   └── art_display.py     # ASCII art renderer
│   │
│   └── utils/
│       ├── __init__.py
│       ├── constants.py        # App constants and defaults
│       └── helpers.py          # Utility functions
│
├── themes/                     # Custom CSS theme files
│   ├── pomodoro-default.tcss  # Default purple theme
│   ├── pomodoro-catppuccin.tcss  # Catppuccin theme
│   ├── pomodoro-nord.tcss     # Nord theme
│   ├── pomodoro-gruvbox.tcss  # Gruvbox theme
│   ├── pomodoro-tokyo-night.tcss  # Tokyo Night theme
│   └── pomodoro-custom.tcss   # User custom theme
│
├── assets/
│   ├── art/                    # ASCII art files
│   │   ├── tomato.txt         # Pomodoro tomato art
│   │   ├── break.txt          # Break time art
│   │   └── focus.txt          # Focus mode art
│   │
│   └── sounds/                 # Audio notification files
│       ├── complete.wav       # Session complete sound
│       └── break.wav          # Break time sound
│
├── config/
│   └── default_config.toml    # Default configuration template
│
└── tests/                      # Unit tests (future)
    ├── __init__.py
    ├── test_timer.py
    └── test_config.py
```

---

## Core Components

### 1. Timer Logic (`src/timer.py`)

**Purpose:** Implement Pomodoro methodology with flexible time settings.

**Classes:**
- `PomodoroTimer`
  - States: IDLE, WORK, SHORT_BREAK, LONG_BREAK, PAUSED
  - Methods:
    - `start()` - Begin a work session
    - `pause()` - Pause current session
    - `resume()` - Resume paused session
    - `stop()` - Stop and reset
    - `skip()` - Skip to next phase
    - `get_remaining_time()` - Returns time left
    - `get_progress()` - Returns progress percentage

**Timer Configuration:**
- Work duration: 25 minutes (adjustable 15-45 min)
- Short break: 5 minutes (adjustable 3-10 min)
- Long break: 15 minutes (adjustable 10-30 min)
- Pomodoros until long break: 4 (adjustable 2-6)

**Events:**
- `on_timer_tick` - Every second update
- `on_session_complete` - Session finished
- `on_break_complete` - Break finished
- `on_cycle_complete` - Full cycle completed

---

### 2. Main Application (`src/app.py`)

**Purpose:** Main Textual application container.

**Class: `PomodoroApp(App)`**

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│          POMODORO TIMER (Header)        │
├─────────────────────────────────────────┤
│                                         │
│         ASCII ART / DECORATION          │
│                                         │
│        ╔═══════════════════╗            │
│        ║    25:00          ║            │
│        ║   FOCUS TIME      ║            │
│        ╚═══════════════════╝            │
│                                         │
│    ████████████████░░░░░░░░ 65%        │
│                                         │
│     Session 2 of 4 before long break    │
│                                         │
├─────────────────────────────────────────┤
│  [Start] [Pause] [Skip] [Settings]     │
└─────────────────────────────────────────┘
```

**Key Bindings:**
- `Space` - Start/Pause
- `s` - Stop/Reset
- `n` - Skip to next phase
- `t` - Toggle theme picker
- `c` - Open settings/config
- `a` - Toggle stats panel
- `q` - Quit application
- `?` - Help screen

**Reactive Properties:**
- `current_time` - Updates every second
- `current_state` - Timer state changes
- `theme_name` - Active theme
- `show_art` - Toggle ASCII art display

---

### 3. Configuration Management (`src/config.py`)

**Purpose:** Load, save, and manage user preferences.

**Config File Location:** `~/.pomodoro-tui/config.toml`

**Configuration Schema:**
```toml
[timer]
work_duration = 25          # minutes
short_break_duration = 5
long_break_duration = 15
pomodoros_until_long_break = 4
auto_start_breaks = false
auto_start_work = false

[appearance]
theme = "pomodoro-default"  # Default purple theme
show_ascii_art = true
ascii_art_style = "tomato"  # tomato, minimal, fancy
show_progress_bar = true
show_session_count = true
animations_enabled = true

[audio]
enabled = true
volume = 0.7
work_complete_sound = "complete.wav"
break_complete_sound = "break.wav"

[statistics]
track_sessions = true
save_history = true
history_file = "~/.pomodoro-tui/history.json"
```

**Functions:**
- `load_config()` - Load from file or create default
- `save_config(config_dict)` - Save to file
- `get_config_value(key, default)` - Get specific value
- `update_config(updates)` - Update and save
- `reset_to_defaults()` - Reset configuration

---

### 4. UI Components

#### 4.1 Timer Display (`src/components/timer_display.py`)

**Widget: `TimerDisplay(Static)`**

**Features:**
- Large, centered time display (MM:SS format)
- Current phase indicator (FOCUS / SHORT BREAK / LONG BREAK)
- Color coding based on phase
- Smooth update animations

**CSS Classes:**
- `.timer-display` - Container
- `.timer-time` - Time text (large)
- `.timer-phase` - Phase label
- `.timer-work` - Work session styling
- `.timer-break` - Break session styling

#### 4.2 Progress Bar (`src/components/progress_bar.py`)

**Widget: `PomodoroProgressBar(ProgressBar)`**

**Features:**
- Visual progress indicator
- Color gradient from start to end
- Percentage display
- Smooth animations

#### 4.3 ASCII Art Display (`src/components/art_display.py`)

**Widget: `ArtDisplay(Static)`**

**Features:**
- Load and display ASCII art from files
- Multiple art styles (tomato, minimal, fancy)
- Color highlighting
- Responsive sizing

**Art Files:**
- `tomato.txt` - Classic pomodoro tomato
- `break.txt` - Coffee cup or relaxation symbol
- `focus.txt` - Concentration symbol

#### 4.4 Settings Panel (`src/components/settings_panel.py`)

**Widget: `SettingsModal(Screen)`**

**Sections:**
- Timer Settings (sliders for durations)
- Appearance Settings (theme picker, toggles)
- Audio Settings (enable/disable, volume)
- About/Help

**Interactive Elements:**
- Sliders for time adjustments
- Checkboxes for toggles
- Theme preview
- Save/Cancel buttons

#### 4.5 Statistics Panel (`src/components/stats_panel.py`)

**Widget: `StatsPanel(Container)`**

**Displays:**
- Today's completed pomodoros
- Total work time today
- Current streak
- Weekly summary
- All-time statistics

---

### 5. Theme System (`themes/*.tcss`)

**Textual CSS (TCSS) Files:**

Each theme file defines:
- Primary, secondary, accent colors
- Background and surface colors
- Text and border colors
- Focus/hover states
- Widget-specific styling

**Example Theme Structure:**
```css
/* pomodoro-nord.tcss */
Screen {
    background: $surface;
}

.timer-display {
    background: $panel;
    border: heavy $primary;
    color: $text;
}

.timer-work {
    color: $error;  /* Red for focus */
}

.timer-break {
    color: $success;  /* Green for break */
}

Button {
    background: $primary;
    color: $text;
}

Button:hover {
    background: $primary-lighten-1;
}
```

**Theme Color References:**
- **Default Purple**: Deep purple (#9d4edd), lavender accents, dark backgrounds
- **Catppuccin Mocha**: Base (#1e1e2e), Mauve (#cba6f7), Lavender (#b4befe), Rosewater (#f5e0dc)
- **Nord**: Polar Night backgrounds (#2e3440), Aurora purples (#b48ead), Frost accents
- **Gruvbox**: Dark background (#282828), Purple (#d3869b), Orange (#fe8019)

**Built-in Themes to Support:**
1. **Pomodoro Default** - Rich purple theme with focus accent colors
2. **Catppuccin** - Soothing pastel purple theme (Mocha variant)
3. **Nord** - Cool blues and muted purples
4. **Gruvbox** - Warm retro colors
5. **Tokyo Night** - Modern dark with neon accents
6. **Custom** - User-defined theme

---

## Development Phases

### Phase 1: Foundation (Core Setup)

**Tasks:**
1. ✅ Create project directory structure
2. Set up Python virtual environment
3. Install dependencies (Textual, Rich, toml)
4. Create `requirements.txt`
5. Implement basic Textual app skeleton
6. Set up configuration system with default TOML
7. Test basic app launch and exit

**Deliverables:**
- Working virtual environment
- Basic app that launches and shows a window
- Configuration loading/saving functionality

**Files to Create:**
- `main.py`
- `src/app.py`
- `src/config.py`
- `src/utils/constants.py`
- `requirements.txt`
- `config/default_config.toml`

---

### Phase 2: Core Timer Logic

**Tasks:**
1. Implement `PomodoroTimer` class
2. Add state management (IDLE, WORK, BREAK, PAUSED)
3. Implement countdown mechanism with threading
4. Add timer events (tick, complete)
5. Test timer accuracy and transitions
6. Implement session cycle tracking (1-4 before long break)

**Deliverables:**
- Fully functional timer logic
- Unit tests for timer states
- Event system working

**Files to Create:**
- `src/timer.py`
- `tests/test_timer.py`

---

### Phase 3: Basic UI Components

**Tasks:**
1. Create `TimerDisplay` widget with large time display
2. Create phase indicator (FOCUS / BREAK)
3. Implement basic layout structure
4. Add control buttons (Start, Pause, Stop, Skip)
5. Wire up button actions to timer logic
6. Add keyboard shortcuts
7. Test UI responsiveness

**Deliverables:**
- Functional timer display updating every second
- Working control buttons
- Keyboard navigation

**Files to Create:**
- `src/components/timer_display.py`
- `src/components/progress_bar.py`

---

### Phase 4: Theming System

**Tasks:**
1. Create default purple TCSS theme file
2. Implement theme loading in app
3. Create Catppuccin theme (MVP priority)
4. Create Nord theme (MVP priority)
5. Create Gruvbox theme (MVP priority)
6. Create Tokyo Night theme
7. Implement theme switcher UI
8. Add theme persistence to config
9. Test theme switching without restart

**Deliverables:**
- Multiple working themes (MVP: Default Purple, Catppuccin, Nord, Gruvbox)
- Live theme switching
- Theme persistence

**Files to Create:**
- `themes/pomodoro-default.tcss` (purple theme)
- `themes/pomodoro-catppuccin.tcss` (Catppuccin Mocha)
- `themes/pomodoro-nord.tcss`
- `themes/pomodoro-gruvbox.tcss`
- `themes/pomodoro-tokyo-night.tcss`
- `src/components/theme_picker.py`

---

### Phase 5: ASCII Art & Visual Effects

**Tasks:**
1. Create ASCII art files (tomato, break, focus)
2. Implement `ArtDisplay` widget
3. Add art loading and rendering
4. Implement progress bar with gradients
5. Add smooth animations for timer updates
6. Create visual phase transitions
7. Add color highlighting to art

**Deliverables:**
- ASCII art displayed beautifully
- Smooth visual effects
- Animated transitions

**Files to Create:**
- `assets/art/tomato.txt`
- `assets/art/break.txt`
- `assets/art/focus.txt`
- `src/components/art_display.py`

---

### Phase 6: Settings Panel

**Tasks:**
1. Create settings modal screen
2. Add sliders for time duration adjustments
3. Implement theme preview in settings
4. Add audio toggles and volume control
5. Create appearance toggles (art, animations)
6. Wire up settings to configuration system
7. Add validation for time ranges
8. Test settings persistence

**Deliverables:**
- Fully functional settings panel
- All settings persisted to config file
- Validation working

**Files to Create:**
- `src/components/settings_panel.py`

---

### Phase 7: Audio Notifications

**Tasks:**
1. Research Windows audio options (winsound vs playsound)
2. Implement audio manager
3. Add sound files or generate tones
4. Play notification on work complete
5. Play notification on break complete
6. Add volume control integration
7. Implement mute functionality
8. Test audio across Windows versions

**Deliverables:**
- Working audio notifications
- Volume control
- Mute toggle

**Files to Create:**
- `src/audio.py`
- `assets/sounds/complete.wav` (or generate)
- `assets/sounds/break.wav` (or generate)

---

### Phase 8: Statistics & Session Tracking

**Tasks:**
1. Implement session statistics tracking
2. Create statistics data model
3. Add JSON persistence for history
4. Create statistics display panel
5. Show daily/weekly/all-time stats
6. Add streak counter
7. Implement data reset functionality
8. Test data accuracy and persistence

**Deliverables:**
- Statistics tracking system
- Visual statistics panel
- Historical data persistence

**Files to Create:**
- `src/stats.py`
- `src/components/stats_panel.py`

---

### Phase 9: Polish & Refinement

**Tasks:**
1. Add help screen with keyboard shortcuts
2. Implement about screen
3. Add loading screen/splash
4. Refine all animations and transitions
5. Optimize performance
6. Add error handling and logging
7. Test edge cases
8. Write user documentation (README)
9. Add comments and docstrings

**Deliverables:**
- Polished, production-ready application
- Complete documentation
- Error handling throughout

**Files to Update:**
- All source files (add docstrings)
- `README.md`

---

### Phase 10: Testing & Distribution

**Tasks:**
1. Write unit tests for core logic
2. Test on different Windows versions
3. Test in different terminals (PowerShell, CMD, Windows Terminal)
4. Create requirements.txt with pinned versions
5. Create installation instructions
6. Test fresh installation
7. Create launcher script (optional)
8. Consider PyInstaller for executable (optional)

**Deliverables:**
- Tested application
- Installation documentation
- Distribution-ready package

---

## Feature Requirements

### Must-Have (MVP)
- ✅ Traditional Pomodoro timer (25-5-15 minutes)
- Timer controls (start, pause, stop, skip)
- Adjustable time settings
- 4 themes (Default Purple, Catppuccin, Nord, Gruvbox)
- Basic ASCII art display
- Progress bar
- Audio notifications
- Configuration persistence
- Keyboard shortcuts

### Should-Have
- Theme switcher with live preview
- Multiple ASCII art styles
- Session cycle tracking (1-4)
- Statistics panel
- Settings modal
- Smooth animations
- Help screen

### Nice-to-Have (Future Enhancements)
- Custom theme creation tool
- Task/note integration (what you're working on)
- Export statistics to CSV
- Multiple timer profiles
- Desktop notifications (Windows Toast)
- System tray integration
- Web dashboard view
- Pomodoro history calendar view
- Focus music integration
- Distraction blocking features

---

## Technical Specifications

### Dependencies

```txt
textual>=0.47.0
rich>=13.7.0
toml>=0.10.2
playsound>=1.3.0  # Fallback for audio
```

### Python Version
- **Minimum:** Python 3.11
- **Recommended:** Python 3.12

### Windows Compatibility
- **Tested on:** Windows 10, Windows 11
- **Terminals:** PowerShell 7, Windows Terminal, CMD
- **Audio:** winsound (built-in) as primary

### Performance Targets
- **Startup time:** < 1 second
- **Memory usage:** < 50MB
- **CPU usage:** < 1% when idle
- **Timer accuracy:** ±1 second over 25 minutes

---

## Testing Strategy

### Unit Tests
- Timer state transitions
- Configuration loading/saving
- Statistics calculations
- Time formatting utilities

### Integration Tests
- Timer + UI integration
- Settings + Config persistence
- Audio + Timer events

### Manual Testing Checklist
- [ ] Timer counts down accurately
- [ ] All keyboard shortcuts work
- [ ] All themes render correctly
- [ ] Audio plays at correct times
- [ ] Settings persist after restart
- [ ] Statistics accumulate correctly
- [ ] App handles window resize
- [ ] App handles Ctrl+C gracefully
- [ ] Works in PowerShell
- [ ] Works in Windows Terminal
- [ ] Works in CMD

---

## Implementation Guidelines for Claude

### Coding Standards
1. **Use type hints** for all function parameters and returns
2. **Add docstrings** to all classes and functions
3. **Follow PEP 8** style guide
4. **Use descriptive variable names**
5. **Keep functions focused** (single responsibility)
6. **Handle errors gracefully** with try/except where appropriate
7. **Use constants** for magic numbers and strings
8. **Comment complex logic** but avoid obvious comments

### Textual Best Practices
1. Use **reactive** properties for dynamic updates
2. Use **compose()** for widget composition
3. Use **on_mount()** for initialization
4. Use **messages** for component communication
5. Use **actions** for keyboard bindings
6. Keep CSS in separate `.tcss` files
7. Use **Screen** for modal dialogs
8. Test with `textual console` for debugging

### Git Workflow (if using Git)
1. Commit after each completed phase
2. Use descriptive commit messages
3. Keep main branch stable
4. Use feature branches for experiments

### User Feedback During Development
1. Ask for approval before major architectural decisions
2. Show visual mockups before implementing complex UI
3. Request theme color preferences
4. Get feedback on ASCII art choices
5. Confirm audio notification sounds are acceptable

---

## Success Criteria

The project is complete when:
- ✅ All Phase 1-8 tasks are completed
- ✅ Application runs without errors
- ✅ All must-have features work correctly
- ✅ 4 MVP themes are implemented (Default Purple, Catppuccin, Nord, Gruvbox)
- ✅ Configuration persists between sessions
- ✅ Audio notifications work
- ✅ Documentation is complete
- ✅ User can customize timer settings
- ✅ Application is visually appealing with purple aesthetic

---

## Notes for Claude

### Before Starting Each Phase:
1. Review the phase tasks and deliverables
2. Ask user if they want to see mockups first (for UI phases)
3. Confirm any color/theme preferences
4. Check if there are any changes to requirements

### During Implementation:
1. Build incrementally - get each component working before moving on
2. Test frequently in the actual terminal
3. Use `textual run --dev` for live CSS reloading
4. Ask for feedback on visual elements before finalizing

### After Completing Each Phase:
1. Test all functionality works
2. Commit code (if using Git)
3. Show demo/screenshot to user if possible
4. Ask if adjustments are needed before proceeding

### Important Reminders:
- Always read files before editing them
- Keep aesthetics as top priority (user's main goal)
- Test in Windows Terminal specifically
- Ask about ASCII art preferences - this is important to the user
- Don't over-engineer - keep it simple and focused
- The goal is personal use, not production software

---

## Quick Start Commands

### Setup Virtual Environment
```bash
cd pomodoro-tui
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Run Application
```bash
python main.py
```

### Run with Dev Mode (CSS live reload)
```bash
textual run --dev main.py
```

### Run Console for Debugging
```bash
textual console
# In another terminal:
python main.py
```

---

## Contact & Support

- **GitHub Issues:** (if open-sourced)
- **Documentation:** README.md in project root
- **Configuration:** Edit `~/.pomodoro-tui/config.toml`

---

*This implementation plan is a living document. Update as needed throughout development.*

**Last Updated:** 2026-01-26
**Version:** 1.1
**Status:** Ready for Phase 1 Implementation

**Changelog:**
- v1.1: Updated default theme to purple, added Catppuccin theme to MVP
- v1.0: Initial implementation plan
