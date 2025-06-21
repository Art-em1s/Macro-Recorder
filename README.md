# Simple Macro Recorder

A simple Python-based mouse macro recorder with GUI interface that allows you to record and replay mouse movements and clicks.

## Features

- Record mouse movements and clicks
- Replay recorded actions
- GUI interface with real-time status updates
- Screen calibration for different display setups
- Keyboard shortcuts for quick control
- Configuration persistence

## Requirements

- Python 3.7+
- Required packages (install via `pip install -r requirements.txt`):
  - pynput
  - tkinter (usually included with Python)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Art-em1s/simple_macro.git
   cd simple_macro
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Easy Launch (Windows)

Simply double-click one of the launcher files:
- `run_macro.bat` - Batch file launcher
- `run_macro.ps1` - PowerShell launcher

### Manual Launch

Run the Python script directly:
```bash
python macro.py
```

### Controls

#### GUI Buttons
- **Start/Stop Recording** - Begin or end recording mouse actions
- **Start/Stop Replay** - Play back recorded actions
- **Manual Calibration** - Calibrate for your screen setup
- **Clear Actions** - Remove all recorded actions

#### Keyboard Shortcuts
- **Left Arrow** - Toggle recording on/off
- **Right Arrow** - Toggle replay on/off
- **Up Arrow** - Start manual calibration
- **Down Arrow** - Exit the application

### Calibration

The app automatically detects your screen resolution, but you can manually calibrate by:
1. Clicking "Manual Calibration" or pressing Up Arrow
2. Clicking the top-left corner of your target area
3. Clicking the bottom-right corner of your target area

## Configuration

Settings are automatically saved to `mouse_recorder_config.json` including:
- Screen dimensions
- Scale factors
- Offset values

## License

This project is open source. Feel free to use and modify as needed.