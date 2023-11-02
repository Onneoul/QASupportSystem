import requests
import flask

class upload_files():
    
    def __init__(self):
        UPLOAD_FOLDER = 'static/Resource'
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'txt', 'log', 'macro', 'performance', 'per'}
    
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
    def request_api(self, url, file_name):
        files = {'file': (file_name.split('/')[-1], open(file_name, 'rb'))}
        response = requests.post(url, files=files)
        print(response.text)
        
    def upload_file(self, file_type, filename):
        
            if not filename:
                print('No file selected')
                return 
            
            if (file_type == 'L'):
                url = 'http://localhost:5000/upload/log'
                request_api(self, url, filename)
                print("log File")
            elif (file_type == 'P'):
                url = 'http://localhost:5000/upload/performance'
                request_api(self, url, filename)
                print("Performance File")
            elif (file_type == 'S'):
                url = 'http://localhost:5000/upload/screenshot'
                request_api(self, url, filename)
                print("Screenshot Macro")
            elif (file_type == 'PM'):
                url = 'http://localhost:5000/upload/playthrough_macro'
                request_api(self, url, filename)
                print("Playthrough Macro")
            elif (file_type == 'M'):
                url = 'http://localhost:5000/upload/macro'
                request_api(self, url, filename)
                print("macros")
                
    
    
    
    
    