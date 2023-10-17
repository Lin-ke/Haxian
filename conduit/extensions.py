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
import datetime
client = Minio(
	endpoint = "localhost:9000",
	access_key= "123",
	secret_key= "12345678",
	secure= False)
# filename 加密过
def uploadpic(filename, data, bucket_name):
    year, month = datetime.datetime.now().strftime("%Y-%m").split("-")
    try:
       client.put_object(bucket_name, "{}/{}/{}".format(year,month,filename), data, len(data))
    except Exception as e:
        print(e)
