import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from game_Info_Manage import game_Info_Manage
from screenshot_App import screenshot_App
from macro import macro
from setting import setting
from login import login_App
import mysql.connector
import configparser

# Config section
config = configparser.ConfigParser()
config.read('config.ini')

# DB
db_host = config.get('database', 'host')
db_port = config.get('database', 'port')
db_username = config.get('database', 'username')
db_password = config.get('database', 'password')

# DB connect
db_connection = mysql.connector.connect(
    host=db_host,
    port=db_port,
    database="autoQA",
    user=db_username,
    password=db_password
)
cursor = db_connection.cursor()

# 로그인 상태 변수
is_logged_in = False

def create_tabs(notebook):
    global is_logged_in

    # Login Tab
    login_tab = ttk.Frame(notebook)
    notebook.add(login_tab, text="Login")
    login_app = login_App(login_tab, db_connection, cursor)

    # Tab 1
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Game Info")
    app1 = game_Info_Manage(tab1)

    # Tab 2
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Screenshot")
    app2 = screenshot_App(tab2)

    # Tab 3
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Macro_Recorder")
    app3 = macro(tab3)

    # Tab 4
    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text="Setting")
    app4 = setting(tab4)

    return app4

def on_tab_change(event):
    global is_logged_in

    selected_tab = notebook.select()
    tab_name = notebook.tab(selected_tab, "text")
    
    if not is_logged_in and tab_name != "Login":
        messagebox.showwarning("Need Login", "Please Login First.")
        notebook.select(0)  # 로그인 탭으로 이동

    elif tab_name == "Setting":
        app.read_config()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Automated QA")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)
    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    app = create_tabs(notebook)

    root.mainloop()