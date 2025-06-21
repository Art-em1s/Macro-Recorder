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
4. **Replay** - Press Right Arrow or click replay button
5. **Repeat** - Actions will loop until you stop replay

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