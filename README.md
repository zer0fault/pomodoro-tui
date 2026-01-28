# 🍅 Pomodoro TUI

A minimalistic terminal-based Pomodoro timer for Windows, built with Python and Textual.

## ✨ Features

- **Traditional Pomodoro Timer**: 25-5-15 minute cycles (fully customizable)
- **Beautiful Themes**: 5 built-in themes including Catppuccin, Nord, Gruvbox, and Tokyo Night
- **Visual Feedback**: Color-coded timer borders (red for work, green for breaks)
- **Audio Notifications**: Subtle beep notifications for session completions
- **Keyboard-First**: Full keyboard control for maximum efficiency
- **Persistent Settings**: Configurations saved automatically

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (Python 3.10+ supported)
- Windows 10/11
- Windows Terminal (recommended), PowerShell, or CMD

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pomodoro-tui.git
cd pomodoro-tui
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## ⌨️ Keyboard Shortcuts

### Timer Controls
- **Space** - Start/Pause timer
- **S** - Stop and reset timer
- **N** - Skip to next phase

### Settings & Customization
- **C** - Open settings panel
- **T** - Open theme picker

### Application
- **?** - Show help screen
- **Q** - Quit application

## ⚙️ Configuration

Settings are stored in `~/.pomodoro-tui/config.toml` and can be modified through the in-app settings panel (press **C**).

### Timer Durations

Adjust work sessions, breaks, and cycle length:
- **Work Duration**: 15-45 minutes (default: 25)
- **Short Break**: 3-10 minutes (default: 5)
- **Long Break**: 10-30 minutes (default: 15)
- **Pomodoros Until Long Break**: 2-6 (default: 4)

### Audio

Toggle audio notifications on/off in the settings panel.

### Themes

Switch themes on-the-fly with the **T** key:
- **Textual Dark** (Default)
- **Catppuccin Mocha** - Soothing pastel theme
- **Nord** - Cool professional blue theme
- **Gruvbox** - Warm retro theme
- **Tokyo Night** - Modern neon theme

## 🎨 Visual Design

The timer uses color-coded borders for instant visual feedback:
- **Red border** - Active work session
- **Green border** - Break time
- **Default border** - Idle state

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **TUI Framework**: [Textual](https://textual.textualize.io/)
- **Audio**: winsound (Windows built-in)
- **Configuration**: TOML

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize
- Inspired by the Pomodoro Technique® by Francesco Cirillo
- Theme colors from [Catppuccin](https://github.com/catppuccin/catppuccin), [Nord](https://www.nordtheme.com/), and [Gruvbox](https://github.com/morhetz/gruvbox)

---

**Made for productive terminal sessions** ☕
