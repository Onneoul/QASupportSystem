import configparser

# configparser ��ü ����
config = configparser.ConfigParser()

# ���� ���� �б�
config.read('config.ini')
config.sections()

print('db' in config)

# ���� �� ���
db_host = config.get('db', 'host')
db_port = config.get('db', 'port')
db_username = config.get('db', 'username')
db_password = config.get('db', 'password')

# �о�� ���� �� ���
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
        