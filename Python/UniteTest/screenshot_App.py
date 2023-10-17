import tkinter as tk
import pyautogui
import keyboard
import os
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector


db_connection = mysql.connector.connect( # DB에 연결
        host="localhost",
        port="3306",
        database="autoQA",
        user="kimminse",
        password="#aB354354"
    )
# db_cursor = db_connection.cursor()
cursor = db_connection.cursor()

class screenshot_App:
    
    def __init__(self, root):
        self.root = root
        # self.root.title("Screenshot App")

        self.start_button = tk.Button(root, text="Start Capture Mode", command=self.start_capture)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Capture Mode", command=self.stop_capture, state=tk.DISABLED)
        self.stop_button.pack()

        self.capture_mode = False
        self.screenshots = []
        self.current_screenshot_idx = 0
        self.popup = None

        keyboard.on_press_key("F2", self.capture_screenshot) # Screenshot 촬영 키 지정

    def start_capture(self):
        self.capture_mode = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.screenshots = []
        self.current_screenshot_idx = 0

    def stop_capture(self):
        self.capture_mode = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.show_screenshots()

    def capture_screenshot(self, event):
        if self.capture_mode:
            screenshot = pyautogui.screenshot()
            self.screenshots.append(screenshot)

    def show_screenshots(self):
        if not self.screenshots:
            return

        # self.root.withdraw()
        
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Screenshot Description")

        screenshot_label = tk.Label(self.popup)
        screenshot_label.pack()

        description_label = tk.Label(self.popup, text="Write a description for the screenshot:")
        description_label.pack()

        description_text = tk.Text(self.popup, height=5, width=40)
        description_text.pack()

        save_button = tk.Button(self.popup, text="Save", command=lambda: self.save_description(description_text, screenshot_label))
        save_button.pack()

        self.show_screenshot_in_popup(screenshot_label)

    def show_screenshot_in_popup(self, label):
        screenshot = self.screenshots[self.current_screenshot_idx]
        screenshot.thumbnail((960, 540))  # Resize the screenshot within 960x540
        screenshot = ImageTk.PhotoImage(screenshot)
        label.config(image=screenshot)
        label.image = screenshot

    def save_description(self, description_text, screenshot_label):
        description = description_text.get("1.0", tk.END).strip()
        description_text.delete("1.0", tk.END)

        screenshot_path = f"screenshot_{self.current_screenshot_idx}.png"
        screenshot_label.config(image=None)

        with open(f"description_{self.current_screenshot_idx}.txt", "w") as f:
            f.write(description)

        # MySQL에 정보 저장
        screenshot_name = f"screenshot_{self.current_screenshot_idx}.png"

        query = "INSERT INTO screenshots (SCREENSHOT_NAME, SCREENSHOT_PATH) VALUES (%s, %s)"
        values = (screenshot_name, screenshot_path)
        self.db_cursor.execute(query, values)
        self.db_connection.commit()

        self.current_screenshot_idx += 1
        if self.current_screenshot_idx < len(self.screenshots):
            self.show_screenshot_in_popup(screenshot_label)
        else:
            self.popup.destroy()
            self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = ScreenshotApp(root)
    # root.mainloop()
    
    # MySQL 연결을 닫음
    # app.db_cursor.close()
    # app.db_connection.close()