# 🍅 Pomodoro TUI

An aesthetic terminal user interface (TUI) Pomodoro timer application for Windows, featuring customizable themes, ASCII art, and rich visual effects.

## ✨ Features

- **Traditional Pomodoro Timer**: 25-5-15 minute cycles with customizable durations
- **Beautiful Themes**: Purple default, Catppuccin, Nord, Gruvbox, and more
- **ASCII Art**: Multiple artistic styles for visual appeal
- **Rich Visual Effects**: Progress bars, animations, and color gradients
- **Audio Notifications**: Sound alerts for session completions
- **Session Tracking**: Statistics and history tracking
- **Keyboard Shortcuts**: Full keyboard control for efficiency

## 🎨 Themes

- **Default Purple**: Rich purple theme with focus accent colors
- **Catppuccin**: Soothing pastel purple (Mocha variant)
- **Nord**: Cool blues and muted purples
- **Gruvbox**: Warm retro colors
- **Tokyo Night**: Modern dark with neon accents (coming soon)

## 🚀 Installation

### Prerequisites

- Python 3.11+ (recommended) or Python 3.10+
- Windows 10/11
- Windows Terminal, PowerShell, or CMD

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pomodoro-tui.git
cd pomodoro-tui
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

Run the application:
```bash
python main.py
```

### Keyboard Shortcuts

- `Space` - Start/Pause timer
- `s` - Stop/Reset timer
- `n` - Skip to next phase
- `t` - Toggle theme picker
- `c` - Open settings
- `a` - Toggle statistics panel
- `q` - Quit application
- `?` - Help screen

## ⚙️ Configuration

Configuration is stored in `~/.pomodoro-tui/config.toml`. You can edit it directly or use the in-app settings panel (press `c`).

### Timer Settings

```toml
[timer]
work_duration = 25              # minutes
short_break_duration = 5
long_break_duration = 15
pomodoros_until_long_break = 4
```

### Appearance Settings

```toml
[appearance]
theme = "pomodoro-default"
show_ascii_art = true
ascii_art_style = "tomato"      # tomato, minimal, fancy
animations_enabled = true
```

## 🛠️ Development

This project is under active development following a phased implementation plan.

### Current Status

- ✅ Phase 1: Foundation (Core Setup) - **COMPLETED**
- ✅ Phase 2: Core Timer Logic - **COMPLETED**
- ✅ Phase 3: Basic UI Components - **COMPLETED & TESTED** ✨
- ✅ Phase 4: Theming System - **COMPLETED & TESTED** 🎨
- ⏳ Phase 5: ASCII Art & Visual Effects
- ⏳ Phase 6: Settings Panel
- ⏳ Phase 7: Audio Notifications
- ⏳ Phase 8: Statistics & Session Tracking

**The timer is fully functional with 5 beautiful themes!**

✨ **What Works:**
- Press Space to start/pause 25-minute focus sessions
- Timer counts down in real-time (MM:SS display)
- Progress bar fills visually as time progresses
- Automatic transitions to breaks after work sessions
- Session counter tracks your progress (1-4 before long break)
- All controls work: Start, Pause, Stop, Skip buttons
- Keyboard shortcuts: Space (start/pause), S (stop), N (skip), T (themes), Q (quit)
- **5 Beautiful Themes**: Switch themes on-the-fly with the T key!
  - Default Purple (calming focus)
  - Catppuccin Mocha (soothing pastels)
  - Nord (cool professional)
  - Gruvbox (warm retro)
  - Tokyo Night (modern neon)

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed development roadmap.

### Technology Stack

- **Language**: Python 3.10+
- **TUI Framework**: Textual (with Rich)
- **Audio**: winsound (Windows native)
- **Configuration**: TOML

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome! Feel free to open an issue or submit a pull request.

## 🙏 Acknowledgments

- Built with [Textual](https://textual.textualize.io/)
- Inspired by the Pomodoro Technique® by Francesco Cirillo
- Theme colors from [Catppuccin](https://github.com/catppuccin/catppuccin), [Nord](https://www.nordtheme.com/), and [Gruvbox](https://github.com/morhetz/gruvbox)

---

**Made with 💜 and ☕ for productive terminal sessions**
