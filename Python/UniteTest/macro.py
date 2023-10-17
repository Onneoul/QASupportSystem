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
        keyboard.add_hotkey('F10', self.save_only)  # F10 키로 지금까지의 매크로만 저장
        self.root = root  # Tkinter root 인스턴스

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
        self.macro_listbox.delete(0, tk.END)  # 기존 목록 삭제
        for file in macro_files:
            self.macro_listbox.insert(tk.END, file)
            
    # F10을 누르면 매크로 액션을 파일에 저장합니다.
    def save_only(self, folder_path):
        # 파일 이름을 현재 시간으로 설정 - 나중에 수정
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"NonPlaythroughMacro_{current_time}.txt"
        file_path = f"{folder_path}/{file_name}"  # 사전에 정의된 폴더 경로

        # 매크로를 파일에 저장
        with open(file_path, "w") as file:
            for action in self.macro_actions:
                file.write(str(action) + "\n")

        # 오버레이 메시지를 표시
        self.show_overlay("Macro saved successfully.")

    # 오버레이 메시지 표시 메서드
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
    app = macro(root)
    root.mainloop()
