import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from game_Info_Manage import game_Info_Manage
from ScreenshotApp import ScreenshotApp
from macro import macro
from setting import setting
from login import login_App
import mysql.connector
import configparser

# Config section
config = configparser.ConfigParser()
config.read('config.ini')
root = None 

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

# login 체크를 위한 class
class LoginStatus:
    def __init__(self):
        self.is_logged_in = False
        self.user_code = None
    
    def set_login_status(self, status, user_code=None):
        self.is_logged_in = status
        self.user_code = user_code
        
        if status:
            create_tabs(notebook, root)
        
login_status = LoginStatus()

def create_tabs(notebook, root):

    for tab in notebook.tabs():
        notebook.forget(tab)

    login_tab = ttk.Frame(notebook)
    notebook.add(login_tab, text="Login")
    login_app = login_App(login_tab, db_connection, cursor, login_status)

    # Tab 1
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Game Info")
    app1 = game_Info_Manage(root, tab1, login_status)

    # Tab 2
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Macro_Recorder")
    app2 = macro(tab2)

    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Setting")
    app3 = setting(tab3)

    return app3

def on_tab_change(event):

    selected_tab = notebook.select()
    tab_name = notebook.tab(selected_tab, "text")
    
    if not login_status.is_logged_in and tab_name != "Login":
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

    app = create_tabs(notebook, root)

    root.mainloop()