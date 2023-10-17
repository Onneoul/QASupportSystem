import tkinter as tk
from pynput import keyboard, mouse
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from datetime import datetime, timedelta
import json
import threading

actions = []
start_time = None
keyboard_controller = KeyboardController()
mouse_controller = MouseController()

def on_press(key):
    global start_time
    elapsed_time = (datetime.now() - start_time).total_seconds()
    actions.append({"type": "key_down", "key": str(key), "time": elapsed_time})

def on_release(key):
    global start_time
    elapsed_time = (datetime.now() - start_time).total_seconds()
    actions.append({"type": "key_up", "key": str(key), "time": elapsed_time})
    if key == keyboard.Key.esc:
        return False

def on_click(x, y, button, pressed):
    global start_time
    elapsed_time = (datetime.now() - start_time).total_seconds()
    actions.append({"type": "mouse", "x": x, "y": y, "button": str(button), "pressed": pressed, "time": elapsed_time})

def start_recording():
    global start_time, actions
    start_time = datetime.now()
    actions = []
    
    with mouse.Listener(on_click=on_click) as mouse_listener:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
            keyboard_listener.join()

    with open("macro.json", "w") as f:
        json.dump(actions, f)

def load_and_execute():
    with open("macro.json", "r") as f:
        recorded_actions = json.load(f)
    
    prev_time = 0
    for action in recorded_actions:
        sleep_time = action["time"] - prev_time
        prev_time = action["time"]
        if sleep_time > 0:
            time.sleep(sleep_time)
        
        if action["type"] == "key_down":
            key = eval(action["key"])
            keyboard_controller.press(key)
        elif action["type"] == "key_up":
            key = eval(action["key"])
            keyboard_controller.release(key)
        elif action["type"] == "mouse":
            x, y = action["x"], action["y"]
            button = eval(f"mouse.{action['button']}")
            mouse_controller.position = (x, y)
            if action["pressed"]:
                mouse_controller.press(button)
            else:
                mouse_controller.release(button)

def start_thread(target):
    thread = threading.Thread(target=target)
    thread.start()

root = tk.Tk()
root.title("Macro Recorder")

start_button = tk.Button(root, text="Start Recording", command=lambda: start_thread(start_recording))
start_button.pack()

load_button = tk.Button(root, text="Load and Execute", command=lambda: start_thread(load_and_execute))
load_button.pack()

root.mainloop()