from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import *
from api.api import server_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.register_blueprint(server_api)
db = SQLAlchemy(app)
from models import *

migrate = Migrate(app,db)

if __name__ == "__main__":
    app.run()

@app.route('/')
def hello():
    return '大海航行靠舵手'
