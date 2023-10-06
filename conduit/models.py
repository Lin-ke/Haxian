from datetime import datetime
from sqlalchemy import  Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_sqlalchemy import SQLAlchemy
from .extensions import db

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,autoincrement=True)
    # 头像url
    name = Column(String(64))
    # 华为id
    wild = Column(String(64),unique = True, nullable=False)
    img_url = Column(Text, default="456")
    phone = Column(Integer)
    email = Column(String(64))
    wx = Column(String(64))
    qq = Column(Integer)
    # 用途：快捷填入
    def __repr__(self):
        return f'<User {self.name!r}>'
class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True,autoincrement=True)
    uid = Column(Integer, ForeignKey(User.id))
    title = Column(String(64))
    text = Column(Text)
    pics = Column(Text)
    status = Column(Integer) # 发出/关闭
    location = Column(String(20))
    date = Column(DateTime)
class Item(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True,autoincrement=True)
    pid = Column(Integer,ForeignKey(Post.id) )
    status = Column(Integer)
    name = Column(String(64))
    text = Column(Text)
    price = Column(Float)
    category = Column(String(64))

class Reply(db.Model):
    __tablename__ = 'reply'
    id = Column(Integer, primary_key=True,autoincrement=True)
    pid = Column(Integer, ForeignKey(Post.id))
    uid = Column(Integer,ForeignKey(User.id))
    status = Column(Integer)
    # json:物品id，价格
    items = Column(Text)
    # json:id，url
    pics = Column(Text)
    text = Column(Text)
    date = Column(DateTime)
