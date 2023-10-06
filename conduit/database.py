# from sqlalchemy import create_engine,MetaData
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from config import Config
# from logger import logger
# from .extensions import db

# logger.info("database start")


# # https://www.cnblogs.com/ChangAn223/p/11277468.html
# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# def init_db():
#     from models import User,Post,Item,Reply
#     Base.metadata.create_all(bind=engine)
# if __name__ == "__main__":
#     init_db()

from sqlalchemy.orm import relationship

from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship
Model = db.Model