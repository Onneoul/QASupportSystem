import os
import keyboard
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import datetime

class macro:

    def __init__(self, root):
        self.root = root

        self.macro_actions = []
        keyboard.add_hotkey('F10', self.save_only)  # F10 Ű�� ���ݱ����� ��ũ�θ� ����
        self.root = root  # Tkinter root �ν��Ͻ�

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

    def record_action(self, e):
        action = {
            "type": e.event_type,
            "input": e.name if e.event_type == keyboard.KEY_DOWN else None,
            "position": pyautogui.position(),
            "timestamp": time.time()
        }
        self.macro_actions.append(action)

    def stop_recording(self):
        keyboard.unhook_all()

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
                for action in actions:
                    eval_action = eval(action)
                    time.sleep(eval_action["timestamp"] - time.time())
                    if eval_action["type"] == keyboard.KEY_DOWN:
                        keyboard.press(eval_action["input"])
                    elif eval_action["type"] == keyboard.KEY_UP:
                        keyboard.release(eval_action["input"])
                    else:
                        pyautogui.moveTo(eval_action["position"])

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_label.config(text="Selected Folder: " + folder_path)
            self.load_macro_files(folder_path)

    def load_macro_files(self, folder_path):
        macro_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
        self.macro_listbox.delete(0, tk.END)  # ���� ��� ����
        for file in macro_files:
            self.macro_listbox.insert(tk.END, file)
            
    # F10�� ������ ��ũ�� �׼��� ���Ͽ� �����մϴ�.
    def save_only(self, folder_path):
        # ���� �̸��� ���� �ð����� ���� - ���߿� ����
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"NonPlaythroughMacro_{current_time}.txt"
        file_path = f"{folder_path}/{file_name}"  # ������ ���ǵ� ���� ���

        # ��ũ�θ� ���Ͽ� ����
        with open(file_path, "w") as file:
            for action in self.macro_actions:
                file.write(str(action) + "\n")

        # �������� �޽����� ǥ��
        self.show_overlay("Macro saved successfully.")

    # �������� �޽��� ǥ�� �޼���
    def show_overlay(self, message):
        overlay = tk.Toplevel(self.root)
        overlay.geometry("300x50+600+400")  # ��ġ�� ũ�� ����
        overlay.attributes("-alpha", 0.8)  # ���� ����
        overlay.attributes("-topmost", True)  # �׻� ���� ǥ��
        tk.Label(overlay, text=message).pack()
        
        # 3�� �Ŀ� �������� ����
        overlay.after(3000, overlay.destroy)
            
if __name__ == "__main__":
    root = tk.Tk()
    app = macro(root)
    root.mainloop()
