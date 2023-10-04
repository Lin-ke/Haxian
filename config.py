# coding = utf-8
import os
class Config:
    """App configuration."""

    JOBS = [
        {
            'id': 'job1',
            'func': 'scheduler:get_access_code',
            'trigger': 'interval',
            'seconds': 7200
        }
    ]

    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///secondhand.db"

DEBUG = True

SECRET_KEY = os.urandom(24)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# mysql配置
# DIALECT = "mysql"
# DRIVER = "pymysql"
# USERNAME = "weiyupeng"
# PASSWORD = "123456"
# HOST = "localhost"
# PORT = "3306"
# DATABASE = "secondhand"

# SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
#                                                                        DATABASE)
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLite配置
