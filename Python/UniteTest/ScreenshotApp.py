import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyautogui
import keyboard
import os
import requests
from datetime import datetime
from PIL import Image, ImageTk
from upload_files import upload_files
import mysql.connector

db_connection = mysql.connector.connect( # DB에 연결
        host="180.83.154.240",
        port="3306",
        database="autoqa",
        user="normal_user_test",
        password="#aB354354@aB354354"
    )
# db_cursor = db_connection.cursor()
cursor = db_connection.cursor()

class ScreenshotApp:
    
    def __init__(self, root=None, create_ui=True, current_test_case_id=None, current_game_version=None):
        
        self.root = root if root else tk.Tk()
        self.current_test_case_id = current_test_case_id
        self.current_game_version = current_game_version
        self.current_bug_case_id = None
        self.capture_mode = False
        self.screenshots = []
        self.current_screenshot_idx = 0
        self.popup = None
        print("screenshotApp Type = %s", type(self.root))
        keyboard.on_press_key("F1", self.capture_screenshot) # Screenshot 촬영 키 지정

        if create_ui:
            self.create_ui()
            
    def create_ui(self):
        self.start_button = tk.Button(self.root, text="Start Capture Mode", command=self.start_capture)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Capture Mode", command=self.stop_capture, state=tk.DISABLED)
        self.stop_button.pack()
        
    def start_capture(self):
        self.capture_mode = True
        if hasattr(self, 'start_button'):  # start_button이 존재하는지 확인
            self.start_button.config(state=tk.DISABLED)
        if hasattr(self, 'stop_button'):  # stop_button이 존재하는지 확인
            self.stop_button.config(state=tk.NORMAL)
        self.screenshots = []
        self.current_screenshot_idx = 0
        print("Current test_case_id = " + self.current_test_case_id)
        print("Current Game Version = " + self.current_game_version)
        

    def stop_capture(self):
        self.capture_mode = False
        if hasattr(self, 'start_button'):  # start_button이 존재하는지 확인
            self.start_button.config(state=tk.NORMAL)
        if hasattr(self, 'stop_button'):  # stop_button이 존재하는지 확인
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
        self.all_screenshots = []
        self.all_descriptions = [] # 스크린샷과 설명 리스트
        
        
        last_bug_case_id = None
        
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("INSERT INTO BUG_CASE (TEST_CASE_ID, BUG_DATE, GAME_VERSION) VALUES (%s, %s, %s)",
                (self.current_test_case_id, datetime.now(), self.current_game_version))
            
            cursor.execute("SELECT BUG_CASE_ID FROM BUG_CASE WHERE TEST_CASE_ID = %s ORDER BY BUG_DATE DESC LIMIT 1", (self.current_test_case_id,))
            last_bug_case_id = cursor.fetchone()[0]
            
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(f"Save Description Transaction failed: {e}")
        
        current_time = datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
        screenshot_path = f"screenshot_{current_time}_{self.current_screenshot_idx:02d}.png"
        self.screenshots[self.current_screenshot_idx].save(screenshot_path) # Save screenshot as file
        screenshot_label.config(image=None)
        
        with open(f"description_{self.current_screenshot_idx}.txt", "w") as f:
            f.write(description)

        # MySQL에 정보 저장
        screenshot_name = screenshot_path
        
        #서버에 업로드
        url = 'http://localhost:5000/upload/screenshot'
        files = {'file': open(screenshot_path, 'rb')}
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            server_path = response.json()['path']
        else:
            messagebox.showinfo("Upload Failed","Failed to upload: {response.content}")
            server_path = None
        
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("INSERT INTO screenshot (SCREENSHOT_NAME, SCREENSHOT_DESCRIPTION, SCREENSHOT_DATE) VALUES (%s, %s, %s)", (screenshot_path, description, datetime.now()))
            cursor.execute("SELECT SCREENSHOT_ID FROM SCREENSHOT WHERE SCREENSHOT_NAME = %s ORDER BY SCREENSHOT_DATE DESC LIMIT 1", (screenshot_name, ))
            last_screenshot_id = cursor.fetchone()[0]
            cursor.execute("COMMIT")
            cursor.execute("UPDATE BUG_CASE SET SCREENSHOT_ID = %s WHERE BUG_CASE_ID = %s", (last_screenshot_id, last_bug_case_id))
            cursor.execute("COMMIT") # Commit 넣기
            print("Successfully saved to the database. bug_case_id = %s, screenshot_id = %s", last_bug_case_id, last_screenshot_id)
            
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(f"GET screenshot ID Transaction failed: {e}")

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
    root.mainloop()