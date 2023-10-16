from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

scheduler = APScheduler()
db = SQLAlchemy()
migrate = Migrate()
# TODO: init through config

from .scheduler import get_access_code
scheduler.add_job(func=get_access_code, trigger='interval', seconds=500, id='getacc', name='getacc', replace_existing=True)

from minio import Minio
client = Minio(
	endpoint = "localhost:9000",
	access_key= "123",
	secret_key= "12345678",
	secure= False)