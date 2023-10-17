import tkinter as tk
from tkinter import ttk, filedialog
#from macro_recorder import *
from screenshot_app import *
from Game_Information_Manage import *

# MySQL 연결을 전역으로 설정
db_connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    database="autoQA",
    user="kimminse",
    password="#aB354354"
)
cursor = db_connection.cursor()

# Tkinter 창 생성
root = tk.Tk()
root.title("Integrated Application")
root.geometry("800x600")

# Notebook 탭 생성
notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
notebook.add(tab1, text="Macro Recorder")
notebook.add(tab2, text="Screenshot")
notebook.add(tab3, text="Game Information Management")
notebook.pack(expand=1, fill='both')

# 각 탭에 대한 내용 정의

# 탭 1: Macro Recorder
folder_label = tk.Label(tab1, text="Selected Folder:")
# ... (add other widgets for the Macro Recorder)
if __name__ == "__main__":
    main_macro()  # Macro Recorder 실행

# 탭 2: Screenshot
start_button = tk.Button(tab2, text="Start Capture Mode", command=ScreenshotApp(root).start_capture)
# ... (add other widgets for the Screenshot)

# 탭 3: Game Information Management
game_combobox = ttk.Combobox(tab3)
# ... (add other widgets for Game Information Management)

# "Run All" 버튼을 클릭하면 현재 탭의 프로그램을 실행함
def run_all_programs():
    current_tab = notebook.index(notebook.select())
    if current_tab == 0:
        main_macro()
    elif current_tab == 1:
        ScreenshotApp(root).start_capture()
    elif current_tab == 2:
        run_game()

run_all_button = tk.Button(root, text="Run Selected Program", command=run_all_programs)
run_all_button.pack()

# 게임 정보 관리 탭을 선택할 때 게임 정보를 로드
def on_tab_select(event):
    current_tab = notebook.index(notebook.select())
    if current_tab == 2:
        load_game_info()

notebook.bind("<<NotebookTabChanged>>", on_tab_select)

# Tkinter 메인 루프 시작
root.mainloop()

# MySQL 연결 종료
db_connection.close()