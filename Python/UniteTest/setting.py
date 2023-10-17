import configparser
import tkinter as tk
from tkinter import ttk, filedialog

class setting:
    
    def __init__(self, root):
        self.root = root
        self.config = configparser.ConfigParser()
        
        database_host_Label = tk.Label(self.root, text="Database Host: ")
        database_host_Label.pack()
        database_host_Entry = tk.Entry(self.root)
        database_host_Entry.pack()
        
        database_port_Label = tk.Label(self.root, text="Database Port: ")
        database_port_Label.pack()
        database_port_Entry = tk.Entry(self.root)
        database_port_Entry.pack()
        
        database_username_Label = tk.Label(self.root, text="Database UserName: ")
        database_username_Label.pack()
        database_username_Entry = tk.Entry(self.root)
        database_username_Entry.pack()
        
        database_password_Label = tk.Label(self.root, text="Database Password: ")
        database_password_Label.pack()
        database_password_Entry = tk.Entry(self.root)
        database_password_Entry.pack()
        
        setting_apply_button = tk.Button(self.root, text="Apply", command=self.write_config)
        setting_apply_button.pack()
        
        
    def read_config(self):
        self.config.read('config.ini')
        
        if self.config.has_section('database'):
            host = self.config.get('database', 'host')
            port = self.config.get('database', 'port')
            username = self.config.get('database', 'username')
            password = self.config.get('database', 'password')

            database_host_Entry.delete(0, tk.END)
            database_host_Entry.insert(0, host)  

            database_port_Entry.delete(0, tk.END)
            database_port_Entry.insert(0, port)

            database_username_Entry.delete(0, tk.END)
            database_username_Entry.insert(0, username)

            database_password_Entry.delete(0, tk.END)
            database_password_Entry.insert(0, password)
        
        
    def write_config(self):
        host = database_host_Entry.get()
        port = database_port_Entry.get()
        username = database_host_Entry.get()
        password = database_password_Entry.get()
        
        self.config['database'] = {'host': host, 'port': port, 'username': username, 'password': password}
        with open('configTest.ini', 'w') as configfile:
            self.config.write(configfile)
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = setting(root)
    root.mainloop()