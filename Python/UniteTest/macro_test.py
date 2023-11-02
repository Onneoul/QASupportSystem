from pynput import keyboard, mouse
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import os

class Macro:

    def __init__(self, root):
        self.macro_actions = []
        self.recording = False
        self.root = root
        self.root.title("Macro Recorder")

        self.record_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.record_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()

        self.save_button = tk.Button(self.root, text="Save Recording", command=self.save_macro)
        self.save_button.pack()

        self.load_play_button = tk.Button(self.root, text="Load and Play", command=self.load_and_play_macro)
        self.load_play_button.pack()

    def start_recording(self):
        self.macro_actions = []
        self.recording = True
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        if self.recording:
            self.macro_actions.append({"type": "key_press", "key": str(key), "timestamp": time.time()})
        if key == keyboard.Key.esc:
            self.stop_recording()
            return False

    def on_release(self, key):
        if self.recording:
            self.macro_actions.append({"type": "key_release", "key": str(key), "timestamp": time.time()})

    def stop_recording(self):
        self.recording = False
        self.listener.stop()

    def save_macro(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for action in self.macro_actions:
                    file.write(str(action) + "\n")
            messagebox.showinfo("Info", "Macro saved successfully.")

    def save_only(self):
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"Macro_{current_time}.txt"
        with open(file_name, "w") as file:
            for action in self.macro_actions:
                file.write(str(action) + "\n")
        self.show_overlay("Macro saved successfully.")

    def load_and_play_macro(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                actions = file.readlines()
                for action in actions:
                    action = eval(action.strip())
                    if action["type"] == "key_press":
                        keyboard.Controller().press(eval(action["key"]))
                    elif action["type"] == "key_release":
                        keyboard.Controller().release(eval(action["key"]))

    def show_overlay(self, message):
        overlay = tk.Toplevel(self.root)
        overlay.geometry("300x50+600+400")  # 위치와 크기 설정
        overlay.attributes("-alpha", 0.8)  # 투명도 설정
        overlay.attributes("-topmost", True)  # 항상 위에 표시
        tk.Label(overlay, text=message).pack()
        
        # 3초 후에 오버레이 제거
        overlay.after(3000, overlay.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = Macro(root)
    root.mainloop()