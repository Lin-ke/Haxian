from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from config import *
from api.api import server_api


app = Flask(__name__)
app.config.from_object(Config())
app.register_blueprint(server_api)
db = SQLAlchemy(app)
from models import *
migrate = Migrate(app,db)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
if __name__ == "__main__":
    app.run()



@app.route('/')
def hello():
    return 'hello, world'
