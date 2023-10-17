import os
import keyboard
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import threading

class macro_recorder:
    
    macro_actions = []

    def record_macro():
        global macro_actions
        macro_actions = []
        keyboard.hook(record_action)

    def record_action(e):
        global macro_actions
        action = {
            "type": e.event_type,
            "input": e.name if e.event_type == keyboard.KEY_DOWN else None,
            "position": pyautogui.position(),
            "timestamp": time.time()
        }
        macro_actions.append(action)

    def stop_recording():
        keyboard.unhook_all()

    def save_macro():
        global macro_actions
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for action in macro_actions:
                    file.write(str(action) + "\n")
            messagebox.showinfo("Info", "Macro saved successfully.")

    def load_and_play_macro():
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

    def select_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_label.config(text="Selected Folder: " + folder_path)
            load_macro_files(folder_path)

    def load_macro_files(folder_path):
        macro_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
        macro_listbox.delete(0, tk.END)  # 기존 목록 삭제
        for file in macro_files:
            macro_listbox.insert(tk.END, file)

    def main():
        root = tk.Tk()
        #윈도우의 타이틀
        root.title("Macro Recorder")
        # 윈도우의 크기 지정
        root.geometry("800x600")

        folder_label = tk.Label(root, text="Selected Folder:")
        folder_label.pack()

        select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
        select_folder_button.pack()
        
        record_button = tk.Button(root, text="Record", command=record_macro)
        record_button.pack()

        stop_button = tk.Button(root, text="Stop", command=stop_recording)
        stop_button.pack()

        save_button = tk.Button(root, text="Save", command=save_macro)
        save_button.pack()

        load_play_button = tk.Button(root, text="Load and Play", command=load_and_play_macro)
        load_play_button.pack()

        macro_listbox = tk.Listbox(root)
        macro_listbox.pack()

        root.mainloop()

    if __name__ == "__main__":
        main()