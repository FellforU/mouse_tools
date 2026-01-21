# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"XCC的鼠小侠" (XCC's Mouse Warrior) is a Python-based Windows mouse automation tool providing three main features:
- Auto-clicker (supports left/middle/right buttons with customizable intervals)
- Mouse Recorder (records and replays mouse movements and clicks)
- Macro System (records complex mouse action sequences with loop support)

**Important:** This tool records precise mouse movements and timing data that could potentially be used to automate actions in games or other applications. Exercise caution when making changes that could enhance automation capabilities.

## Development Commands

### Running the Application
```bash
python example_usage.py
```

### Building Executable
```bash
pip install pyinstaller
python script/build_exe.py
```

Or directly:
```bash
pyinstaller example_usage.py --name="XCC的鼠小侠" --windowed --onefile --clean --noconfirm --icon=mouse.ico
```

### Dependencies
- `pynput` - Mouse and keyboard input handling
- `Pillow` (PIL) - Image processing for icons
- `tkinter` - GUI (built into Python)

## Architecture

### Main Entry Point
- `example_usage.py` - Simple launcher that creates and runs the main `MouseApp` instance

### Core Application (mouse_recorder.py)

The application uses a tabbed interface with three main modules:

1. **MouseApp** - Main window and auto-clicker functionality
   - Manages keyboard hotkeys for all modules
   - Auto-clicker runs in a separate thread using `threading.Thread`

2. **MouseRecorder** - Records and plays back mouse sequences
   - Events stored with precise timing in milliseconds
   - Recordings saved as JSON files in `recordings/` directory
   - Hotkeys: F8 (record), F9 (playback)

3. **MouseMacro** - Creates and executes complex action sequences
   - Macros stored as JSON files in `macros/` directory
   - Supports editing individual action delays
   - Loop execution support (0 = infinite)
   - Hotkeys: F7 (record), F6 (execute)

### Data Storage Format

Both recordings and macros use a JSON-based event format with:
- `type`: "move" or "click"
- `x`, `y`: Screen coordinates
- `button`: Mouse button (for click events)
- `pressed`: Boolean (for click events)
- `delay`: Time in milliseconds since previous event

Example:
```json
{"type": "move", "x": 892, "y": 310, "delay": 107}
{"type": "click", "x": 880, "y": 269, "button": "Button.left", "pressed": true, "delay": 130}
```

### Thread Safety

All background operations (auto-clicking, replay, macro execution) run in daemon threads using `threading.Thread`. The `is_running`, `is_clicking`, or `is_replaying` flags are used to signal thread termination.

### Directory Structure
```
mouse_tools/
├── example_usage.py           # Entry point
├── mouse_recorder.py          # Main application (all classes)
├── mouse.ico                  # Application icon
├── mouse_actions.json         # Pre-recorded action data
├── README.txt                 # User documentation
├── macros/                    # User-created macros (created on first run)
├── recordings/                # User recordings (created on first run)
└── script/
    ├── build_exe.py           # PyInstaller build script
    ├── create_icon.py         # Icon generation
    ├── convert_icon.py        # Icon conversion
    └── fix_git_encoding.py    # Git encoding fix
```

## Code Patterns

### Keyboard Hotkey Handling
All modules use `pynput.keyboard.Listener` for global hotkey detection. Hotkey names are stored as `StringVar` for GUI binding.

### Mouse Event Recording
Both `MouseRecorder` and `MouseMacro` use `pynput.mouse.Listener` with callbacks:
- `on_move(x, y)` - Records position changes
- `on_click(x, y, button, pressed)` - Records button presses

### JSON File Operations
All data files are read/written using Python's built-in `json` module. Files are created on-demand using `os.makedirs(..., exist_ok=True)`.

### GUI Framework
Uses `tkinter` with `ttk` widgets for a native Windows look. Key patterns:
- `ttk.Notebook` for tabbed interface
- `ttk.Treeview` for lists (recordings, macros, actions)
- `Toplevel` for modal dialogs
- Context menus using `Menu` with `tearoff=0`

## Important Notes

- The application creates `recordings/` and `macros/` directories automatically on first run
- All coordinates are absolute screen positions
- Delays are stored in milliseconds but converted to seconds for `time.sleep()`
- The `button_map` dictionary converts button strings to `pynput.mouse.Button` objects
- Windows-specific (uses `os.environ['TK_SILENCE_DEPRECATION'] = '1'` for tk)
