import tkinter as tk
from tkinter import filedialog, messagebox
import requests

class upload_files:
    
    def __init__(self):
        pass

    def upload_file(self, file_type, files, test_case_id):
        if not files:
            print('No file selected')
            return
        url = None
        
        # files = {'file': (filename.split('/')[-1], open(filename, 'rb'))}
        data = {'test_case_id': test_case_id}
        # File Type 선택
        if (file_type == 'L'):
            url = 'http://localhost:5000/upload/log'
            print("log File")
        elif (file_type == 'P'):
            url = 'http://localhost:5000/upload/performance'
            print("Performance File")
        elif (file_type == 'S'):
            url = 'http://localhost:5000/upload/screenshot'
            print("Screenshot Macro")
        elif (file_type == 'PM'):
            url = 'http://localhost:5000/upload/playthrough_macro'
            print("Playthrough Macro")
        elif (file_type == 'M'):
            url = 'http://localhost:5000/upload/macro'
            print("macros")
            
        try:
            response = requests.post(url, files=files, data=data)
            messagebox.showinfo("Success", response.text)
        except Exception as e:
            messagebox.showinfo("Failed", str(e))
         

if __name__ == "__main__":
    # Tkinter UI
    root = tk.Tk()
    root.title('File Upload')
    filename = None
    # select_button = tk.Button(root, text='Select File', command=select_file)
    # select_button.pack()
    # upload_button = tk.Button(root, text='Upload File', command=upload_file)
    # upload_button.pack()
    root.mainloop()