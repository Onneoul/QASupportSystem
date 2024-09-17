import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from upload_files import upload_files
from ScreenshotApp import ScreenshotApp
import os
import mysql.connector
import subprocess
import threading
import time
import datetime


db_connection = mysql.connector.connect( # DB에 연결
        host="180.83.154.240",
        port="3306",
        database="autoqa",
        user="normal_user_test",
        password="#aB354354@aB354354"
    )
cursor = db_connection.cursor() # 테스트용, 나중에 제거

class game_Info_Manage:

    def __init__(self, root, frame, login_status):
        self.root = root
        self.frame = frame
        self.current_test_case_id = None 
        self.login_status = login_status
        self.user_code = self.login_status.user_code
        print("login status ", self.login_status)
        

        self.create_ui()
    

    # UI 생성
    def create_ui(self):
        self.game_combobox = ttk.Combobox(self.frame)
        self.game_combobox.pack()

        # Add_Game_Info를 눌렀을 때, 게임 정보 추가를 위한 GUI 생성
        def open_add_game_window():
            add_game_window = tk.Toplevel(self.frame)
            add_game_window.title("Add Game Info")
            add_game_window.geometry("600x400")

            def add_game_info():
                title = game_title_entry.get()
                exe_path = game_exe_path.get()
                version = game_version_entry.get()
                try:
                    cursor.execute("INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH) VALUES (%s, %s, %s)", (title, version, exe_path))
                    cursor.execute('COMMIT')
                    add_game_window.destroy()
                    print("Game information added successfully!")
                    load_game_info()  # 게임 정보를 추가한 후 Combobox 새로고침
                except Exception as e:
                    print("Error occurred while adding game information:", str(e))

            game_title_label = tk.Label(add_game_window, text="Game Title:")
            game_title_label.pack()

            game_title_entry = tk.Entry(add_game_window)
            game_title_entry.pack()

            game_exe_label = tk.Label(add_game_window, text="Game Execution Location:")
            game_exe_label.pack()

            game_exe_path = tk.StringVar()

            def select_game_exe():
                file_path = filedialog.askopenfilename(filetypes=[("Execution File", "*.exe")])
                if file_path:
                    game_exe_path.set(file_path)

            game_exe_entry = tk.Entry(add_game_window, textvariable=game_exe_path)
            game_exe_entry.pack()

            browse_button = tk.Button(add_game_window, text="Browse", command=select_game_exe)
            browse_button.pack()

            game_version_label = tk.Label(add_game_window, text="Game Version:")
            game_version_label.pack()

            game_version_entry = tk.Entry(add_game_window)
            game_version_entry.pack()

            add_button = tk.Button(add_game_window, text="Add", command=add_game_info)
            add_button.pack()

        add_button = tk.Button(self.frame, text="Game Info Add", command=open_add_game_window)
        add_button.pack()

        def load_game_info():
            cursor.execute("SELECT GAME_TITLE, GAME_VERSION FROM GAME_INFORMATION")
            games = cursor.fetchall()
            self.game_combobox['values'] = [" | ".join(game) for game in games]
        
        load_game_info()
        self.game_combobox.pack()
        run_button = tk.Button(self.frame, text="Run", command=self.run_game)
        run_button.pack()
        
# File Upload 섹션
        
    
    # Game 실행 섹션

        # def run_game():
        #     selected_game = game_combobox.get().split(" | ")[0]
        #     selected_game_version = game_combobox.get().split(" | ")[1]
        #     cursor.execute("SELECT GAME_EXECUTION_PATH FROM GAME_INFORMATION WHERE GAME_TITLE = %s and GAME_VERSION = %s", (selected_game, selected_game_version))
        #     exe_path = cursor.fetchone()[0]
        
        #     try:
        #         subprocess.Popen(exe_path)
        #     except Exception as e:
        #         print("Error occur while execute Game:", str(e))

        # run_button = tk.Button(self.root, text="Run", command=run_game)
        # run_button.pack()
    
    # DB에서 게임 실행 경로를 읽어와 실행. 상대 경로로 만들까?
    def run_game(self):
        
        selected_game = self.game_combobox.get().split(" | ")[0]
        selected_game_version = self.game_combobox.get().split(" | ")[1]
        cursor.execute("SELECT GAME_EXECUTION_PATH FROM GAME_INFORMATION WHERE GAME_TITLE = %s and GAME_VERSION = %s", (selected_game, selected_game_version))
        exe_path = cursor.fetchone()[0]
        
        try:
            try:
                cursor.execute("START TRANSACTION")
                # 시퀀스 테이블에 값을 삽입
                cursor.execute("INSERT INTO SEQUENCE () VALUES ()")
                db_connection.commit()
                # 가장 최근의 시퀀스 값을 가져옴
                cursor.execute("SELECT LAST_INSERT_ID()")
                sequence = cursor.fetchone()[0]
                # 트랜잭션 커밋
                cursor.execute("COMMIT")
            except Exception as e:
                cursor.execute("ROLLBACK")
                messagebox.showinfo("Sequence Error", "RollBACK" + str(e))
                
            # TEST_CASE_ID 생성
            self.current_test_case_id = "T" + time.strftime("%Y%m%d") + f"{sequence:03d}"  # 세 자리 시퀀스
            self.screenshot_app = ScreenshotApp(root=self.root, create_ui=False, current_test_case_id=self.current_test_case_id, current_game_version=selected_game_version)
            self.screenshot_app.start_capture()
            # TEST_CASE 테이블에 삽입
            cursor.execute("INSERT INTO TEST_CASE (TEST_CASE_ID, TEST_DATE, GAME_VERSION, USER_CODE) VALUES (%s, %s, %s, %s)",
                        (self.current_test_case_id, datetime.datetime.now(), selected_game_version, self.user_code))
            db_connection.commit()
            
                        
            # 게임 실행 섹션
            try:
                game_process = subprocess.Popen(exe_path)
                monitoring_thread = threading.Thread(target=self.monitor_game_process, args=(game_process,)) # 게임을 실행하며 다른 스레드에서 monitor_game_process를 실행
                monitoring_thread.start()
            except Exception as e:
                messagebox.showinfo("Error occurred while executing the game:", str(e))
                
        except Exception as e:
            messagebox.showinfo("Create Test case Error", str(e))


    # 게임 종료 감지
    def monitor_game_process(self, game_process):
        while True:
            exit_code = game_process.poll()
            if exit_code is not None:
                print(f"The game has terminated with exit code {exit_code}")
                self.UploadFiles()  # 게임이 종료되면 UploadFiles 메서드를 호출
                self.screenshot_app.stop_capture()
                break
            time.sleep(1)
            
    def UploadFiles(self):
        upload_window = tk.Toplevel(self.root)
        upload_window.title("Upload Files")
        upload_window.geometry("400x400")

        log_file_path = tk.StringVar()
        perf_file_path = tk.StringVar()
        ptMacro_file_path = tk.StringVar()

        def select_log_file():
            file_path = filedialog.askopenfilename(filetypes=[("Log File", "*.log")])
            if file_path:
                log_file_path.set(file_path)

        def select_perf_file():
            file_path = filedialog.askopenfilename(filetypes=[("Performance File", "*.txt")])
            if file_path:
                perf_file_path.set(file_path)

        def select_playthrough_macro():
            file_path = filedialog.askopenfilename(filetypes=[("Playthrough Macro File", "*.txt")])
            if file_path:
                ptMacro_file_path.set(file_path)

        def upload_to_server():
            log_path = log_file_path.get()
            print('log_path = ' + log_path)
            perf_path = perf_file_path.get()
            ptMacro_path = ptMacro_file_path.get()
            
            log_filename = os.path.basename(log_path)
            perf_filename = os.path.basename(perf_path)
            ptMacro_filename = os.path.basename(ptMacro_path)
            
            uploader = upload_files()

            try:
                # log 파일 업로드
                log_files = {'file': (log_filename, open(log_path, 'rb'))} 
                uploader.upload_file('L', log_files, self.current_test_case_id)

                # Performance 파일 업로드
                perf_files = {'file': (perf_filename, open(perf_path, 'rb'))}
                uploader.upload_file('P', perf_files, self.current_test_case_id)

                # Macro 파일 업로드
                ptMacro_files = {'file': (ptMacro_filename, open(ptMacro_path, 'rb'))}
                uploader.upload_file('PM', ptMacro_files, self.current_test_case_id)
                messagebox.showinfo("Upload Status", "Files uploaded successfully!")  # 혹은 실패한 파일에 대한 정보도 추가
            
                upload_window.destroy()
                
            except Exception as e:
                print("Error occurred while uploading files:", str(e))

        # 파일 업로드 GUI
        log_file_label = tk.Label(upload_window, text="Select Log File:")
        log_file_label.pack()
        log_file_entry = tk.Entry(upload_window, textvariable=log_file_path)
        log_file_entry.pack()
        browse_log_button = tk.Button(upload_window, text="Browse", command=select_log_file)
        browse_log_button.pack()
        perf_file_label = tk.Label(upload_window, text="Select Performance File:")
        perf_file_label.pack()
        perf_file_entry = tk.Entry(upload_window, textvariable=perf_file_path)
        perf_file_entry.pack()
        browse_perf_button = tk.Button(upload_window, text="Browse", command=select_perf_file)
        browse_perf_button.pack()
        perf_file_label = tk.Label(upload_window, text="Select Playthrough Macro File:")
        perf_file_label.pack()
        perf_file_entry = tk.Entry(upload_window, textvariable=ptMacro_file_path)
        perf_file_entry.pack()
        browse_perf_button = tk.Button(upload_window, text="Browse", command=select_playthrough_macro)
        browse_perf_button.pack()
        upload_button = tk.Button(upload_window, text="Upload", command=upload_to_server)
        upload_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = game_Info_Manage(root)
    root.mainloop()