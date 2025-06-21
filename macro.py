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

# Hide console window on Windows
if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

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
            # Control keys for the application
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
            # Record keyboard events during recording (if enabled)
            elif self.recording and getattr(self, 'keyboard_recording_enabled', True):
                current_time = time.time()
                try:
                    # Try to get the character representation
                    key_name = key.char if hasattr(key, 'char') and key.char else key.name
                except AttributeError:
                    key_name = str(key).replace('Key.', '')
                
                self.actions.append(('keypress', key_name, True, current_time - self.last_action_time))
                self.last_action_time = current_time
                self.log(f"Recorded key press: {key_name}")
        except AttributeError:
            pass
    
    def on_release(self, key):
        if self.recording and getattr(self, 'keyboard_recording_enabled', True):
            try:
                current_time = time.time()
                try:
                    # Try to get the character representation
                    key_name = key.char if hasattr(key, 'char') and key.char else key.name
                except AttributeError:
                    key_name = str(key).replace('Key.', '')
                
                self.actions.append(('keypress', key_name, False, current_time - self.last_action_time))
                self.last_action_time = current_time
                self.log(f"Recorded key release: {key_name}")
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

                if action[0] == 'move':
                    scaled_x = (action[1] - self.offset_x) / self.scale_x
                    scaled_y = (action[2] - self.offset_y) / self.scale_y
                    self.mouse.position = (int(scaled_x), int(scaled_y))
                elif action[0] == 'click':
                    scaled_x = (action[1] - self.offset_x) / self.scale_x
                    scaled_y = (action[2] - self.offset_y) / self.scale_y
                    self.mouse.position = (int(scaled_x), int(scaled_y))
                    
                    if action[4]:  # pressed
                        self.mouse.press(action[3])
                        self.log(f"Replayed {'right' if action[3] == Button.right else 'left'} click at ({scaled_x}, {scaled_y})")
                    else:
                        self.mouse.release(action[3])
                elif action[0] == 'keypress':
                    key_name, pressed = action[1], action[2]
                    
                    try:
                        # Handle special keys
                        if len(key_name) == 1:
                            # Single character key
                            key_obj = key_name
                        else:
                            # Special key (like 'enter', 'space', etc.)
                            key_obj = getattr(Key, key_name.lower(), key_name)
                        
                        if pressed:
                            self.keyboard.press(key_obj)
                            self.log(f"Replayed key press: {key_name}")
                        else:
                            self.keyboard.release(key_obj)
                            self.log(f"Replayed key release: {key_name}")
                    except Exception as e:
                        self.log(f"Error replaying key {key_name}: {e}")

    def run(self):
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click) as mouse_listener, \
             keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as keyboard_listener:
            
            self.log("Press Up Arrow key to start calibration.")
            self.log("Press Left Arrow key to start/stop recording.")
            self.log("Press Right Arrow key to start/stop replaying actions.")
            self.log("Press Down Arrow key to exit.")

            keyboard_listener.join()

class MacroRecorderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Macro Recorder")
        self.root.geometry("750x500")  # Increased width to accommodate all buttons + 50px
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
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_btn = ttk.Button(button_frame, text="Save Macro", command=self.save_macro)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.load_btn = ttk.Button(button_frame, text="Load Macro", command=self.load_macro)
        self.load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Keyboard recording toggle
        self.keyboard_enabled = tk.BooleanVar(value=True)
        self.keyboard_checkbox = ttk.Checkbutton(
            button_frame, 
            text="Record Keyboard", 
            variable=self.keyboard_enabled,
            command=self.toggle_keyboard_recording
        )
        self.keyboard_checkbox.pack(side=tk.LEFT)
        
        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(anchor=tk.W)
        
        self.actions_label = ttk.Label(status_frame, text="Actions recorded: 0")
        self.actions_label.pack(anchor=tk.W)
        
        self.config_label = ttk.Label(status_frame, text="")
        self.config_label.pack(anchor=tk.W)
        
        # Actions display with editing capabilities
        actions_frame = ttk.LabelFrame(main_frame, text="Recorded Actions", padding="5")
        actions_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.rowconfigure(0, weight=1)
        
        # Create treeview for actions
        columns = ('Type', 'Key/Button', 'X', 'Y', 'Action', 'Delay (s)')
        self.actions_tree = ttk.Treeview(actions_frame, columns=columns, show='headings', height=8)
        
        # Configure column headings
        self.actions_tree.heading('Type', text='Type')
        self.actions_tree.heading('Key/Button', text='Key/Button')
        self.actions_tree.heading('X', text='X')
        self.actions_tree.heading('Y', text='Y')
        self.actions_tree.heading('Action', text='Action')
        self.actions_tree.heading('Delay (s)', text='Delay (s)')
        
        # Configure column widths
        self.actions_tree.column('Type', width=70)
        self.actions_tree.column('Key/Button', width=80)
        self.actions_tree.column('X', width=50)
        self.actions_tree.column('Y', width=50)
        self.actions_tree.column('Action', width=70)
        self.actions_tree.column('Delay (s)', width=80)
        
        # Add scrollbar to treeview
        tree_scrollbar = ttk.Scrollbar(actions_frame, orient=tk.VERTICAL, command=self.actions_tree.yview)
        self.actions_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.actions_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Action editing buttons
        edit_frame = ttk.Frame(actions_frame)
        edit_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.edit_timing_btn = ttk.Button(edit_frame, text="Edit Timing", command=self.edit_timing)
        self.edit_timing_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_action_btn = ttk.Button(edit_frame, text="Delete Selected", command=self.delete_selected_action)
        self.delete_action_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.move_up_btn = ttk.Button(edit_frame, text="Move Up", command=self.move_action_up)
        self.move_up_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.move_down_btn = ttk.Button(edit_frame, text="Move Down", command=self.move_action_down)
        self.move_down_btn.pack(side=tk.LEFT)
        
        # Log display (smaller now)
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, width=70)
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
        self.refresh_actions_display()
    
    def edit_timing(self):
        selection = self.actions_tree.selection()
        if not selection:
            self.update_log("Please select an action to edit timing")
            return
        
        item = selection[0]
        action_index = int(self.actions_tree.index(item))
        
        if action_index >= len(self.recorder.actions):
            self.update_log("Invalid action selected")
            return
            
        current_delay = self.recorder.actions[action_index][-1]
        
        # Create timing edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Action Timing")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        ttk.Label(dialog, text=f"Edit delay for action {action_index + 1}:").pack(pady=10)
        
        delay_var = tk.StringVar(value=str(current_delay))
        delay_entry = ttk.Entry(dialog, textvariable=delay_var, width=20)
        delay_entry.pack(pady=5)
        delay_entry.focus()
        delay_entry.select_range(0, tk.END)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def save_timing():
            try:
                new_delay = float(delay_var.get())
                if new_delay < 0:
                    raise ValueError("Delay cannot be negative")
                
                # Update the action's delay
                action = list(self.recorder.actions[action_index])
                action[-1] = new_delay
                self.recorder.actions[action_index] = tuple(action)
                
                self.update_log(f"Updated action {action_index + 1} delay to {new_delay:.3f}s")
                self.refresh_actions_display()
                dialog.destroy()
            except ValueError as e:
                self.update_log(f"Invalid delay value: {e}")
        
        def cancel_edit():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_timing).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to save
        dialog.bind('<Return>', lambda e: save_timing())
        dialog.bind('<Escape>', lambda e: cancel_edit())
    
    def delete_selected_action(self):
        selection = self.actions_tree.selection()
        if not selection:
            self.update_log("Please select an action to delete")
            return
        
        item = selection[0]
        action_index = int(self.actions_tree.index(item))
        
        if action_index >= len(self.recorder.actions):
            self.update_log("Invalid action selected")
            return
        
        # Remove the action
        del self.recorder.actions[action_index]
        self.update_log(f"Deleted action {action_index + 1}")
        self.refresh_actions_display()
        self.update_status()
    
    def move_action_up(self):
        selection = self.actions_tree.selection()
        if not selection:
            self.update_log("Please select an action to move")
            return
        
        item = selection[0]
        action_index = int(self.actions_tree.index(item))
        
        if action_index == 0:
            self.update_log("Action is already at the top")
            return
        
        if action_index >= len(self.recorder.actions):
            self.update_log("Invalid action selected")
            return
        
        # Swap with previous action
        actions = self.recorder.actions
        actions[action_index], actions[action_index - 1] = actions[action_index - 1], actions[action_index]
        
        self.update_log(f"Moved action {action_index + 1} up")
        self.refresh_actions_display()
        
        # Reselect the moved item
        new_item = self.actions_tree.get_children()[action_index - 1]
        self.actions_tree.selection_set(new_item)
    
    def move_action_down(self):
        selection = self.actions_tree.selection()
        if not selection:
            self.update_log("Please select an action to move")
            return
        
        item = selection[0]
        action_index = int(self.actions_tree.index(item))
        
        if action_index >= len(self.recorder.actions) - 1:
            self.update_log("Action is already at the bottom")
            return
        
        # Swap with next action
        actions = self.recorder.actions
        actions[action_index], actions[action_index + 1] = actions[action_index + 1], actions[action_index]
        
        self.update_log(f"Moved action {action_index + 1} down")
        self.refresh_actions_display()
        
        # Reselect the moved item
        new_item = self.actions_tree.get_children()[action_index + 1]
        self.actions_tree.selection_set(new_item)
    
    def refresh_actions_display(self):
        # Clear existing items
        for item in self.actions_tree.get_children():
            self.actions_tree.delete(item)
        
        # Add actions to treeview
        for i, action in enumerate(self.recorder.actions):
            action_type = action[0]
            
            if action_type == 'move':
                x, y, delay = action[1], action[2], action[3]
                self.actions_tree.insert('', 'end', values=('Mouse', '-', x, y, 'Move', f"{delay:.3f}"))
            elif action_type == 'click':
                x, y, button, pressed, delay = action[1], action[2], action[3], action[4], action[5]
                button_text = 'Right' if button.name == 'right' else 'Left'
                press_text = 'Press' if pressed else 'Release'
                self.actions_tree.insert('', 'end', values=('Mouse', button_text, x, y, press_text, f"{delay:.3f}"))
            elif action_type == 'keypress':
                key_name, pressed, delay = action[1], action[2], action[3]
                press_text = 'Press' if pressed else 'Release'
                self.actions_tree.insert('', 'end', values=('Keyboard', key_name, '-', '-', press_text, f"{delay:.3f}"))
    
    def save_macro(self):
        if not self.recorder.actions:
            self.update_log("No actions to save")
            return
        
        from tkinter import filedialog
        import datetime
        
        # Generate default filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"macro_{timestamp}.json"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Macro",
            initialvalue=default_name
        )
        
        if file_path:
            try:
                # Convert actions to serializable format
                serializable_actions = []
                for action in self.recorder.actions:
                    if action[0] == 'click':
                        # Convert button object to string
                        action_list = list(action)
                        action_list[3] = action[3].name  # Convert button to string
                        serializable_actions.append(action_list)
                    elif action[0] == 'keypress':
                        # Keyboard actions are already serializable
                        serializable_actions.append(list(action))
                    else:
                        # Mouse move actions
                        serializable_actions.append(list(action))
                
                macro_data = {
                    'actions': serializable_actions,
                    'created': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'action_count': len(self.recorder.actions)
                }
                
                with open(file_path, 'w') as f:
                    json.dump(macro_data, f, indent=2)
                
                self.update_log(f"Macro saved to {file_path}")
            except Exception as e:
                self.update_log(f"Error saving macro: {e}")
    
    def load_macro(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Macro"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    macro_data = json.load(f)
                
                if 'actions' not in macro_data:
                    self.update_log("Invalid macro file format")
                    return
                
                # Convert back to proper format
                loaded_actions = []
                for action in macro_data['actions']:
                    if action[0] == 'click':
                        # Convert button string back to button object
                        action[3] = Button.right if action[3] == 'right' else Button.left
                        loaded_actions.append(tuple(action))
                    elif action[0] == 'keypress':
                        # Keyboard actions are already in correct format
                        loaded_actions.append(tuple(action))
                    else:
                        # Mouse move actions
                        loaded_actions.append(tuple(action))
                
                self.recorder.actions = loaded_actions
                self.refresh_actions_display()
                self.update_status()
                
                created = macro_data.get('created', 'Unknown')
                action_count = len(loaded_actions)
                self.update_log(f"Loaded macro with {action_count} actions (created: {created})")
                
            except Exception as e:
                self.update_log(f"Error loading macro: {e}")
    
    def toggle_keyboard_recording(self):
        enabled = self.keyboard_enabled.get()
        self.recorder.keyboard_recording_enabled = enabled
        status = "enabled" if enabled else "disabled"
        self.update_log(f"Keyboard recording {status}")
        
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
        
        # Refresh actions display if actions count changed
        current_action_count = len(self.actions_tree.get_children())
        if current_action_count != len(self.recorder.actions):
            self.refresh_actions_display()
        
        self.root.after(100, self.update_status)
        
    def update_log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def run(self):
        self.update_log("Macro Recorder started")
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
