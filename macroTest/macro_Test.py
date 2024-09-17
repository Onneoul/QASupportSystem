from tkinter import Tk, Button, filedialog
from pynput import mouse, keyboard
import pyautogui
import json
import time

recorded_actions = []
mouse_listener = None
keyboard_listener = None

def on_click(x, y, button, pressed):
    action = {
        'type': 'mouse',
        'x': x,
        'y': y,
        'button': str(button),
        'pressed': pressed,
        'timestamp': time.time()
    }
    recorded_actions.append(action)

def on_key_press(key):
    action = {
        'type': 'keyboard',
        'key': str(key),
        'pressed': True,
        'timestamp': time.time()
    }
    recorded_actions.append(action)

def on_key_release(key):
    action = {
        'type': 'keyboard',
        'key': str(key),
        'pressed': False,
        'timestamp': time.time()
    }
    recorded_actions.append(action)

def start_recording():
    global recorded_actions
    recorded_actions = []
    global mouse_listener, keyboard_listener
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    
    mouse_listener.start()
    keyboard_listener.start()

def stop_recording():
    global mouse_listener, keyboard_listener
    mouse_listener.stop()
    keyboard_listener.stop()
    
    # Show file dialog for saving
    filepath = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if filepath:
        with open(filepath, 'w') as f:
            json.dump(recorded_actions, f)

def play_macro():
    # Show file dialog for opening
    filepath = filedialog.askopenfilename(defaultextension=".json",
                                          filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if filepath:
        with open(filepath, 'r') as f:
            actions = json.load(f)
        
        prev_timestamp = actions[0]['timestamp']

        for action in actions:
            sleep_time = action['timestamp'] - prev_timestamp
            time.sleep(sleep_time)
            
            if action['type'] == 'mouse':
                pyautogui.moveTo(action['x'], action['y'])
                if action['pressed']:
                    pyautogui.mouseDown(button=action['button'].split('.')[1].lower())
                else:
                    pyautogui.mouseUp(button=action['button'].split('.')[1].lower())
                    
            elif action['type'] == 'keyboard':
                key = action['key'].replace("'", "")
                if 'Key.' in key:
                    key = key.split('.')[1]
                if action['pressed']:
                    pyautogui.keyDown(key)
                else:
                    pyautogui.keyUp(key)

            prev_timestamp = action['timestamp']

# GUI setup
root = Tk()
root.title('Macro Recorder')

start_button = Button(root, text="Start Recording", command=start_recording)
stop_button = Button(root, text="Stop Recording", command=stop_recording)
play_button = Button(root, text="Play Macro", command=play_macro)

start_button.pack()
stop_button.pack()
play_button.pack()

root.mainloop()