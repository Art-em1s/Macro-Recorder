# 🖱️ Simple Macro Recorder

A powerful yet simple Python-based mouse macro recorder with an intuitive GUI interface. Perfect for automating repetitive mouse tasks, testing applications, or creating demonstrations.

## ✨ Features

- 🎯 **Precise Recording** - Capture mouse movements and clicks with accurate timing
- 🔄 **Seamless Playback** - Replay recorded actions with configurable scaling
- 🖥️ **Clean GUI Interface** - User-friendly interface with real-time status updates
- 📐 **Smart Calibration** - Automatic screen detection with manual calibration options
- ⌨️ **Keyboard Shortcuts** - Quick control without touching the mouse
- 💾 **Persistent Settings** - Configuration automatically saved between sessions
- 🔇 **Silent Operation** - Run without console windows for clean execution
- 📋 **Action Editor** - Interactive list showing all recorded actions with detailed information
- ⏱️ **Timing Control** - Edit delays between actions with precision timing editor
- 🗑️ **Action Management** - Delete, reorder, and modify individual actions
- 💾 **Macro Save/Load** - Export and import macros with JSON format and metadata
- 🔄 **Real-time Updates** - Live action list that updates as you record
- ⌨️ **Keyboard Recording** - Capture and replay keyboard events with optional toggle control
- 🎹 **Mixed Input Support** - Record both mouse and keyboard actions in a single macro

## 🚀 Quick Start

### Windows Users (Recommended)
1. **Download** the latest release or clone this repository
2. **Install Python** 3.7+ from [python.org](https://python.org)
3. **Install dependencies**: Open command prompt in the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```
4. **Launch the app** by double-clicking:
   - `run_macro_silent.vbs` - **Completely silent** (recommended)
   - `run_macro.bat` - Background launch
   - `run_macro.ps1` - PowerShell launcher

### Alternative Launch Methods
```bash
# Direct Python execution
python macro.py

# Silent execution (Windows)
pythonw macro.py
```

## 🎮 How to Use

### GUI Controls
| Button | Function |
|--------|----------|
| **Start/Stop Recording** | Begin or end recording mouse actions |
| **Start/Stop Replay** | Play back recorded actions |
| **Manual Calibration** | Calibrate for your specific screen setup |
| **Clear Actions** | Remove all recorded actions |
| **Save Macro** | Export current macro to JSON file with timestamp |
| **Load Macro** | Import previously saved macro from JSON file |
| **Edit Timing** | Modify delay for selected action in the list |
| **Delete Selected** | Remove selected action from the sequence |
| **Move Up/Down** | Reorder actions in the sequence |
| **Record Keyboard** | Toggle checkbox to enable/disable keyboard event recording |

### Keyboard Shortcuts (Global)
| Key | Action |
|-----|--------|
| `←` Left Arrow | Toggle recording on/off |
| `→` Right Arrow | Toggle replay on/off |
| `↑` Up Arrow | Start manual calibration |
| `↓` Down Arrow | Exit application |

### Recording Workflow
1. **Start Recording** - Click the record button or press Left Arrow
2. **Perform Actions** - Move mouse and click as needed
3. **Stop Recording** - Click record button again or press Left Arrow
4. **Edit Actions** (Optional):
   - View all actions in the interactive list
   - Select any action to edit its timing delay
   - Delete unwanted actions or reorder the sequence
   - Fine-tune your macro for perfect execution
5. **Save Macro** (Optional) - Export your macro with automatic timestamped filename
6. **Replay** - Press Right Arrow or click replay button
7. **Repeat** - Actions will loop until you stop replay

### Action Editing Features
- **Interactive Action List**: View all recorded actions with Type, Key/Button, Coordinates, Action, and Delay columns
- **Mixed Input Display**: Mouse and keyboard actions shown together in chronological order
- **Precision Timing**: Edit individual action delays with millisecond precision
- **Sequence Management**: Delete unwanted actions or reorder them with move up/down
- **Macro Persistence**: Save and load macros with metadata including creation time and action count

### Keyboard Support
- **Full Keyboard Recording**: Capture all key presses and releases including special keys
- **Character Keys**: Letters, numbers, symbols, and punctuation
- **Special Keys**: Enter, Space, Tab, Ctrl, Alt, Shift, function keys, and more
- **Toggle Control**: Enable/disable keyboard recording with the "Record Keyboard" checkbox
- **Mixed Macros**: Combine mouse movements, clicks, and keyboard input in a single macro
- **Accurate Playback**: Precise timing and key state reproduction during replay

## ⚙️ Configuration & Calibration

### Automatic Setup
The application automatically detects your screen resolution and configures appropriate scaling factors.

### Manual Calibration
For precise control across different screen setups:
1. Click **"Manual Calibration"** or press `↑` Up Arrow
2. Click the **top-left corner** of your target area
3. Click the **bottom-right corner** of your target area
4. Calibration complete! Settings are automatically saved.

### Configuration File
Settings are stored in `mouse_recorder_config.json`:
```json
{
  "scale_x": 1.0,
  "scale_y": 1.0,
  "offset_x": 0,
  "offset_y": 0,
  "screen_width": 1920,
  "screen_height": 1080
}
```

### Macro File Format
Saved macros use JSON format with metadata:
```json
{
  "actions": [
    ["move", 100, 200, 0.1],
    ["click", 150, 250, "left", true, 0.5],
    ["keypress", "h", true, 0.2],
    ["keypress", "h", false, 0.1],
    ["keypress", "enter", true, 0.3],
    ["keypress", "enter", false, 0.1]
  ],
  "created": "2024-12-21 14:30:52",
  "action_count": 6
}
```

## 🛠️ Installation & Requirements

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **Dependencies**: Listed in `requirements.txt`

### Detailed Installation
1. **Clone Repository**:
   ```bash
   git clone https://github.com/Art-em1s/simple_macro.git
   cd simple_macro
   ```

2. **Create Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**:
   ```bash
   python macro.py
   ```

## 🔧 Troubleshooting

### Common Issues

**"Permission denied" or security warnings**
- On macOS: Grant accessibility permissions in System Preferences > Security & Privacy
- On Windows: Run as administrator if needed
- Some antivirus software may flag automation tools

**Playback not accurate**
- Use manual calibration for precise control
- Ensure consistent screen resolution between recording and playback

**Application won't start**
- Verify Python 3.7+ is installed: `python --version`
- Check all dependencies are installed: `pip install -r requirements.txt`
- Try running with: `python -m tkinter` to test GUI support

## 📋 Use Cases

- **Software Testing** - Automate repetitive UI testing scenarios
- **Demonstrations** - Create consistent product demos
- **Accessibility** - Assist users with mobility limitations
- **Gaming** - Automate repetitive game tasks (check game's ToS)
- **Data Entry** - Speed up form filling and data input tasks

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## ⭐ Support

If you find this tool useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for automation enthusiasts**