from datetime import datetime
from sqlalchemy import  Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_sqlalchemy import SQLAlchemy
from .extensions import db

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True,autoincrement=True)
    # 头像url
    name = Column(String(64), default="")
    # 华为id
    wlid = Column(String(64),unique = True, nullable=False)
    img_url = Column(Text, default="")
    phone = Column(String(16),default="")
    email = Column(String(64),default="")
    signature = Column(String(64),default="")
    wx = Column(String(64),default="")
    qq = Column(String(16),default="")
    # 用途：快捷填入
    def __repr__(self):
        return f'<User {self.name!r}>'
class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'post'
    pid = Column(Integer, primary_key=True,autoincrement=True)
    kind = Column(Integer)  # 1是出，2是收
    uid = Column(Integer, ForeignKey(User.uid))
    title = Column(String(64), default="")
    text = Column(Text)
    pics = Column(Text)
    status = Column(Integer,default=1) # 发出/关闭
    location = Column(String(20), default="")
    date = Column(DateTime)
    search = Column(Text)
class Item(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'item'
    iid = Column(Integer, primary_key=True,autoincrement=True)
    pid = Column(Integer,ForeignKey(Post.pid) )
    status = Column(Integer,default=1)
    name = Column(String(64), default="")
    text = Column(Text)
    price = Column(Integer) # 分为单位
    category = Column(String(64), default="")

class Reply(db.Model):
    __tablename__ = 'reply'
    __table_args__ = {'extend_existing': True}
    rid = Column(Integer, primary_key=True,autoincrement=True)
    pid = Column(Integer, ForeignKey(Post.pid))
    uid = Column(Integer,ForeignKey(User.uid))
    status = Column(Integer,default=1)
    # json:物品id，价格
    items = Column(Text)
    # json:id，url
    pics = Column(Text)
    text = Column(Text)
    date = Column(DateTime)
class Favorite(db.Model):
    __tablename__ = "favorite"
    __table_args__ = {'extend_existing': True}
    fid = Column(Integer, primary_key=True,autoincrement=True)
    pid = Column(Integer, ForeignKey(Post.pid))
    uid = Column(Integer,ForeignKey(User.uid))
    date = Column(DateTime)
# kv
class Goods(db.Model):
    __tablename__ = 'goods'
    __table_args__ = {'extend_existing': True}
    gid = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(64), default="")
    text = Column(Text,default="")
    barcode = Column(String(16),default="")
    category = Column(String(64), default="")

class Complaint(db.Model):
    __tablename__ = 'complaint'
    __table_args__ = {'extend_existing': True}
    cid = Column(Integer, primary_key=True,autoincrement=True)
    pid = Column(Integer, ForeignKey(Post.pid))
    uid = Column(Integer,ForeignKey(User.uid))
    text = Column(Text)
    date = Column(DateTime)
    status = Column(Integer,default=1) # 1是未处理，2是已处理
    result = Column(Text,default="") # 处理结果
class Ban(db.Model):
    __tablename__ = 'ban'
    __table_args__ = {'extend_existing': True}
    bid = Column(Integer, primary_key=True,autoincrement=True)
    uid = Column(Integer,ForeignKey(User.uid))
    date = Column(DateTime)
    enddate = Column(DateTime)