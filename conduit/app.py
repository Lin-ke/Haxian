from flask import Flask
from .config import *
from api.api import server_api
from api.gentoken import token_api
from .exceptions import InvalidUsage
from flask_cors import CORS
# extensions 是flask扩展
# logger也可以放进去



# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from conduit.extensions import db, migrate, scheduler


from conduit.config import Config


def create_app(config_object=Config()):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    
    app = Flask(__name__.split('.')[0])
    CORS(app)
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    from .scheduler import get_access_code
    get_access_code()
    register_extensions(app)
    register_models(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app):
    from .logger import logger
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)    
    scheduler.start()
    logger.info("start server. init finished.")
def register_models(app):
        # 注册Models
    from .models import User,Post,Item,Reply,Favorite

def register_blueprints(app):
    """Register Flask blueprints."""
    CORS(server_api)
    CORS(token_api)
    app.register_blueprint(server_api)
    app.register_blueprint(token_api)

def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)

