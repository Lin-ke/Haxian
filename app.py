from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from config import *
from api.api import server_api
from api.gentoken import token_api
from scheduler import get_access_code

app = Flask(__name__)
app.config.from_object(Config())
app.register_blueprint(server_api)
app.register_blueprint(token_api)
db = SQLAlchemy(app)
from models import *
migrate = Migrate(app,db)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
if __name__ == "__main__":
    get_access_code()

    app.run()



@app.route('/')
def hello():
    return 'hello, world'
