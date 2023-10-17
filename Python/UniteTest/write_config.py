import configparser

config = configparser.ConfigParser()

config['db'] = {'host': 'localhost', 'port': '3306', 'username': 'kimminse', 'password': '#aB354354'}

with open('config.ini', 'w') as configfile:
    config.write(configfile)