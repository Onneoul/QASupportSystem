import tkinter as tk
from tkinter import ttk, filedialog
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

class Game_Information_Manage:

    # Tkinter 창 생성
    root = tk.Tk()
    root.title("Game Information Management")
    root.geometry("600x400")

    # Game Information Selection ComboBox
    game_combobox = ttk.Combobox(root)
    game_combobox.pack()

    # 게임 정보 입력 창을 열기 위한 함수
    def open_add_game_window():
        add_game_window = tk.Toplevel(root)
        add_game_window.title("Add Game Info")
        add_game_window.geometry("600x400")

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

        game_log_label = tk.Label(add_game_window, text="Log Path:")
        game_log_label.pack()

        game_log_path = tk.StringVar()

        def select_game_log():
            folder_path = filedialog.askdirectory()
            if folder_path:
                game_log_path.set(folder_path)

        game_log_entry = tk.Entry(add_game_window, textvariable=game_log_path)
        game_log_entry.pack()

        browse_log_button = tk.Button(add_game_window, text="Browse", command=select_game_log)
        browse_log_button.pack()

        def add_game_info():
            title = game_title_entry.get()
            exe_path = game_exe_path.get()
            version = game_version_entry.get()
            log_path = game_log_path.get()
        try:
            # MySQL에 게임 정보 추가
            sql = "INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH, GAME_LOG_PATH) VALUES (%s, %s, %s, %s)"
            val = (title, version, exe_path, log_path)
            cursor.execute(sql, val)
            db_connection.commit()
            add_game_window.destroy()
            print("Game information added successfully!")
        except Exception as e:
            # 만약 예외가 발생하면 예외 메시지를 출력
            print("Error occurred while adding game information:", str(e))

        add_button = tk.Button(add_game_window, text="Add", command="add_game_info")
        add_button.pack()

    # "추가" 버튼을 클릭하여 게임 정보 창을 열기 위한 버튼
    add_button = tk.Button(root, text="Game Info Add", command=open_add_game_window)
    add_button.pack()

    # ComboBox 및 게임 실행 버튼
    def load_game_info():
        cursor.execute("SELECT GAME_TITLE, GAME_VERSION FROM GAME_INFORMATION")
        games = cursor.fetchall()
        game_combobox['values'] = [" | ".join(game) for game in games]
        
    load_game_info()
    game_combobox.pack()

    #Run Game Button
    def run_game():
        selected_game = game_combobox.get().split(" | ")[0]
        selected_game_version = game_combobox.get().split(" | ")[1]
        cursor.execute("SELECT GAME_EXECUTION_PATH FROM GAME_INFORMATION WHERE GAME_TITLE = %s and GAME_VERSION = %s", (selected_game, selected_game_version))
        exe_path = cursor.fetchone()[0]
        
        try:
            # 게임 실행 파일을 실행
            subprocess.Popen(exe_path)
        except Exception as e:
            # 게임 실행 중 오류 발생 시 처리
            print("Error occur while execute Game:", str(e))

    run_button = tk.Button(root, text="Run", command="") #run_game
    run_button.pack()
