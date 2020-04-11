import os

SECRET_KEY = os.urandom(24)
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'   # 改为自己的数据库用户名
PASSWORD = 'root'   # 改为自己的数据库密码
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'blog'   # 改为自己新建的schema名

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
