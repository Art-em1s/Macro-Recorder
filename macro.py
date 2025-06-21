import time
import threading
import json
import os
import ctypes
import tkinter as tk
from tkinter import ttk, scrolledtext
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

class MouseRecorderRepeater:
    def __init__(self, gui_callback=None):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.actions = []
        self.recording = False
        self.repeating = False
        self.calibrating = False
        self.exit_flag = False
        self.last_action_time = None
        self.calibration_points = []
        self.config_file = 'mouse_recorder_config.json'
        self.gui_callback = gui_callback
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.scale_x = config.get('scale_x', 1)
            self.scale_y = config.get('scale_y', 1)
            self.offset_x = config.get('offset_x', 0)
            self.offset_y = config.get('offset_y', 0)
            self.screen_width = config.get('screen_width', 1920)
            self.screen_height = config.get('screen_height', 1080)
            self.log(f"Loaded configuration: Scale ({self.scale_x}, {self.scale_y}), Offset ({self.offset_x}, {self.offset_y})")
        else:
            self.detect_screen_info()

    def save_config(self):
        config = {
            'scale_x': self.scale_x,
            'scale_y': self.scale_y,
            'offset_x': self.offset_x,
            'offset_y': self.offset_y,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        self.log(f"Saved configuration to {self.config_file}")

    def detect_screen_info(self):
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            
            self.screen_width = root.winfo_screenwidth()
            self.screen_height = root.winfo_screenheight()
            
            if os.name == 'nt':
                user32 = ctypes.windll.user32
                user32.SetProcessDPIAware()
                
            self.scale_x = 1.0
            self.scale_y = 1.0
            self.offset_x = 0
            self.offset_y = 0
            
            root.destroy()
            
            self.log(f"Auto-detected screen: {self.screen_width}x{self.screen_height}")
            self.save_config()
        except Exception as e:
            self.log(f"Error detecting screen info: {e}")
            self.screen_width = 1920
            self.screen_height = 1080
            self.scale_x = 1.0
            self.scale_y = 1.0
            self.offset_x = 0
            self.offset_y = 0

    def log(self, message):
        print(message)
        if self.gui_callback:
            self.gui_callback(message)

    def on_press(self, key):
        try:
            if key == Key.left:
                self.toggle_recording()
            elif key == Key.right:
                self.toggle_repeating()
            elif key == Key.up:
                self.start_calibration()
            elif key == Key.down:
                self.log("Exiting...")
                self.exit_flag = True
                self.repeating = False
                return False
        except AttributeError:
            pass

    def start_calibration(self):
        if not self.calibrating:
            self.log("Starting calibration. Click on the top-left corner of your screen, then the bottom-right corner.")
            self.calibrating = True
            self.calibration_points = []

    def on_click(self, x, y, button, pressed):
        if self.calibrating and pressed:
            self.calibration_points.append((x, y))
            if len(self.calibration_points) == 1:
                self.log("Top-left corner recorded. Now click on the bottom-right corner.")
            elif len(self.calibration_points) == 2:
                self.calculate_calibration()
                self.calibrating = False
        elif self.recording:
            current_time = time.time()
            self.actions.append(('click', x, y, button, pressed, current_time - self.last_action_time))
            self.last_action_time = current_time
            if pressed:
                self.log(f"Recorded {'right' if button == Button.right else 'left'} click at ({x}, {y})")

    def calculate_calibration(self):
        tl_x, tl_y = self.calibration_points[0]
        br_x, br_y = self.calibration_points[1]
        screen_width = br_x - tl_x
        screen_height = br_y - tl_y
        self.scale_x = screen_width / self.screen_width
        self.scale_y = screen_height / self.screen_height
        self.offset_x = tl_x
        self.offset_y = tl_y
        self.log(f"Calibration complete. Scale: ({self.scale_x}, {self.scale_y}), Offset: ({self.offset_x}, {self.offset_y})")
        self.save_config()

    def toggle_recording(self):
        if not self.recording:
            self.log("Recording started...")
            self.actions = []
            self.recording = True
            self.last_action_time = time.time()
        else:
            self.recording = False
            self.log(f"Recording stopped. {len(self.actions)} actions recorded.")

    def toggle_repeating(self):
        if not self.repeating:
            if self.actions:
                self.log("Replaying actions...")
                self.repeating = True
                threading.Thread(target=self.repeat_actions, daemon=True).start()
            else:
                self.log("No actions recorded yet.")
        else:
            self.repeating = False
            self.log("Replaying stopped.")

    def on_move(self, x, y):
        if self.recording:
            current_time = time.time()
            self.actions.append(('move', x, y, current_time - self.last_action_time))
            self.last_action_time = current_time

    def repeat_actions(self):
        while self.repeating and not self.exit_flag:
            for action in self.actions:
                if not self.repeating or self.exit_flag:
                    break

                time.sleep(action[-1])

                if action[0] in ('move', 'click'):
                    scaled_x = (action[1] - self.offset_x) / self.scale_x
                    scaled_y = (action[2] - self.offset_y) / self.scale_y
                    self.mouse.position = (int(scaled_x), int(scaled_y))
                    
                    if action[0] == 'click':
                        if action[4]:  # pressed
                            self.mouse.press(action[3])
                            self.log(f"Replayed {'right' if action[3] == Button.right else 'left'} click at ({scaled_x}, {scaled_y})")
                        else:
                            self.mouse.release(action[3])

    def run(self):
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click) as mouse_listener, \
             keyboard.Listener(on_press=self.on_press) as keyboard_listener:
            
            self.log("Press Up Arrow key to start calibration.")
            self.log("Press Left Arrow key to start/stop recording.")
            self.log("Press Right Arrow key to start/stop replaying actions.")
            self.log("Press Down Arrow key to exit.")

            keyboard_listener.join()

class MacroRecorderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Macro Recorder")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.recorder = MouseRecorderRepeater(gui_callback=self.update_log)
        self.start_listeners()
        self.update_status()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.record_btn = ttk.Button(button_frame, text="Start Recording", command=self.toggle_recording)
        self.record_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.replay_btn = ttk.Button(button_frame, text="Start Replay", command=self.toggle_replay)
        self.replay_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.calibrate_btn = ttk.Button(button_frame, text="Manual Calibration", command=self.start_calibration)
        self.calibrate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(button_frame, text="Clear Actions", command=self.clear_actions)
        self.clear_btn.pack(side=tk.LEFT)
        
        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(anchor=tk.W)
        
        self.actions_label = ttk.Label(status_frame, text="Actions recorded: 0")
        self.actions_label.pack(anchor=tk.W)
        
        self.config_label = ttk.Label(status_frame, text="")
        self.config_label.pack(anchor=tk.W)
        
        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Keyboard shortcuts info
        info_frame = ttk.LabelFrame(main_frame, text="Keyboard Shortcuts", padding="5")
        info_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        shortcuts_text = ("Left Arrow: Toggle Recording | Right Arrow: Toggle Replay\n"
                         "Up Arrow: Manual Calibration | Down Arrow: Exit")
        ttk.Label(info_frame, text=shortcuts_text).pack(anchor=tk.W)
        
        # Keyboard listener will be started after recorder is created
        
    def start_listeners(self):
        def start_recorder():
            self.recorder.run()
            
        self.recorder_thread = threading.Thread(target=start_recorder, daemon=True)
        self.recorder_thread.start()
        
    def toggle_recording(self):
        self.recorder.toggle_recording()
        self.update_status()
        
    def toggle_replay(self):
        self.recorder.toggle_repeating()
        self.update_status()
        
    def start_calibration(self):
        self.recorder.start_calibration()
        self.update_status()
        
    def clear_actions(self):
        self.recorder.actions = []
        self.update_log("Actions cleared")
        self.update_status()
        
    def update_status(self):
        if self.recorder.recording:
            status = "🔴 Recording..."
            self.record_btn.config(text="Stop Recording")
        else:
            status = "⚪ Ready"
            self.record_btn.config(text="Start Recording")
            
        if self.recorder.repeating:
            status += " | 🔄 Replaying..."
            self.replay_btn.config(text="Stop Replay")
        else:
            self.replay_btn.config(text="Start Replay")
            
        if self.recorder.calibrating:
            status += " | 🎯 Calibrating..."
            
        self.status_label.config(text=status)
        self.actions_label.config(text=f"Actions recorded: {len(self.recorder.actions)}")
        
        config_text = (f"Screen: {self.recorder.screen_width}x{self.recorder.screen_height} | "
                      f"Scale: ({self.recorder.scale_x:.2f}, {self.recorder.scale_y:.2f})")
        self.config_label.config(text=config_text)
        
        self.root.after(100, self.update_status)
        
    def update_log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def run(self):
        self.update_log("Mouse Macro Recorder started")
        self.update_log("Use buttons above or keyboard shortcuts")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.recorder.exit_flag = True

if __name__ == "__main__":
    app = MacroRecorderGUI()
    app.run()
