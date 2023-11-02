import os
import keyboard
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import threading

class macro:

    def __init__(self, root):
        self.root = root
        self.macro_actions = []
        keyboard.add_hotkey('F10', self.save_only)

        self.folder_label = tk.Label(root, text="Selected Folder:")
        self.folder_label.pack()

        self.select_folder_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack()

        self.record_button = tk.Button(root, text="Record", command=self.record_macro)
        self.record_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recording)
        self.stop_button.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_macro)
        self.save_button.pack()

        self.load_play_button = tk.Button(root, text="Load and Play", command=self.load_and_play_macro)
        self.load_play_button.pack()

        self.macro_listbox = tk.Listbox(root)
        self.macro_listbox.pack()

    def record_macro(self):
        self.macro_actions = []
        keyboard.hook(self.record_action)
        self.mouse_thread = threading.Thread(target=self.record_mouse_position)
        self.mouse_thread.start()

    def record_mouse_position(self):
        while True:
            x, y = pyautogui.position()
            self.macro_actions.append({
                "type": "mouse_move",
                "position": (x, y),
                "timestamp": time.monotonic()
            })
            time.sleep(0.1)

    def record_action(self, e):
        action = {
            "type": e.event_type,
            "input": e.name,
            "timestamp": time.monotonic()
        }
        self.macro_actions.append(action)

    def stop_recording(self):
        keyboard.unhook_all()
        self.mouse_thread.join()

    def save_macro(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for action in self.macro_actions:
                    file.write(str(action) + "\n")
            messagebox.showinfo("Info", "Macro saved successfully.")

    def load_and_play_macro(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                actions = file.readlines()
                prev_time = None
                for action in actions:
                    eval_action = eval(action.strip())
                    cur_time = eval_action["timestamp"]

                    if prev_time is not None:
                        time.sleep(cur_time - prev_time)

                    prev_time = cur_time

                    if eval_action["type"] == "key_down":
                        keyboard.press(eval_action["input"])
                    elif eval_action["type"] == "key_up":
                        keyboard.release(eval_action["input"])
                    elif eval_action["type"] == "mouse_move":
                        x, y = eval_action["position"]
                        pyautogui.moveTo(x, y)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_label.config(text="Selected Folder: " + folder_path)
            self.load_macro_files(folder_path)

    def load_macro_files(self, folder_path):
        macro_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
        self.macro_listbox.delete(0, tk.END)
        for file in macro_files:
            self.macro_listbox.insert(tk.END, file)

    def save_only(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for action in self.macro_actions:
                    file.write(str(action) + "\n")

    def show_overlay(self, message):
        overlay = tk.Toplevel(self.root)
        overlay.geometry("300x50+600+400")
        overlay.attributes("-alpha", 0.8)
        overlay.attributes("-topmost", True)
        tk.Label(overlay, text=message).pack()
        overlay.after(3000, overlay.destroy)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = macro(root)
    root.mainloop()