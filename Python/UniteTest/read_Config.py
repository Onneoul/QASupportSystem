import configparser

# configparser 객체 생성
config = configparser.ConfigParser()

# 설정 파일 읽기
config.read('config.ini')
config.sections()

print('db' in config)

# 설정 값 얻기
db_host = config.get('db', 'host')
db_port = config.get('db', 'port')
db_username = config.get('db', 'username')
db_password = config.get('db', 'password')

# 읽어온 설정 값 사용
print(f"db Host: {db_host}")
print(f"db Port: {db_port}")
print(f"db Username: {db_username}")
print(f"db Password: {db_password}")

class read_settings:
    
    def read_db_host(self):
        self.db_host = config.get('db', 'host')
        return self.db_host
    def read_db_port(self):
        self.db_port = config.get('db', 'port')
        return self.db_port
    def read_db_username(self):
        self.db_username = config.get('db', 'username')
        return self.db_username
    def read_db_password(self):
        self.db_password = config.get('db', 'password')
        return self.db_password
        