import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class login_App:

    def __init__(self, root, db_connection, cursor):
        self.root = root
        self.db_connection = db_connection
        self.cursor = cursor
        
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_username = ttk.Label(self.frame, text="Username:")
        self.label_username.grid(row=0, column=0)
        self.entry_username = ttk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1)

        self.label_password = ttk.Label(self.frame, text="Password:")
        self.label_password.grid(row=1, column=0)
        self.entry_password = ttk.Entry(self.frame, show="*")
        self.entry_password.grid(row=1, column=1)

        self.button_login = ttk.Button(self.frame, text="Login", command=self.check_login)
        self.button_login.grid(row=2, columnspan=2)

    def check_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Successfully logged in!")
            # 성공적으로 로그인 한 후의 코드를 여기에 작성
        else:
            messagebox.showerror("Failed", "Invalid username or password")