from typing import Dict
from flask import Blueprint, session, request,g,Response,jsonify
import json
from sqlalchemy import select
from api import auth
from conduit.database import db
from conduit.models import User,Post,Item,Reply
from conduit.logger import logger
from api.utils import *
import datetime
import time
server_api = Blueprint('api_data', __name__)
# return : id, name (test)
@server_api.route('/api/getdata')
def get_user_data():
    result, info = auth.verify_token(g.get("token"))
    if result:
        user_id = info["id"]
        user_name = info["name"]
    # 查询：db.session.query(User).filter(User.id == user_id).first()
    user_name = "John1"
    # result = db.session.execute(select(User).where(User.id == user_id))
    result = db.session.query(User).filter(User.name == user_name).first()
    if result is None:
        return jsonify({
            "err" : 0,
            "data" : {
        }})
    return jsonify(
        {
            "err": 0,
            "data": {
                "id": result.id,
                "name": result.name
            }
        }
    )

@server_api.route('/api/posts')
def get_posts():
    try:
        if request.method == "POST":
            data = request.json
            kind:int = data.get("kind")
            keywords = data.get("kind")
            category = data.get("category")
            items = db.session.query(Item).filter(Item.category == category).all()
            pids = []
            for item in items:
                pids.append(item.__dict__["pid"])
            posts = db.session.query(Post).filter(Post.pid.in_(pids))
            posts = posts.filter(Post.kind == kind)
            for keyword in keywords:
                posts.filter(Post.text.like(f"%{keyword}%"))
            results = posts.all()
            return jsonify(posts_dict(results))
    except:
        return jsonify({"err" : 1})
    return jsonify({"err" : 1})

@server_api.route('/api/post')
def get_post():
    try:
        if request.method == "GET":
            pid = request.args.get("pid")
            post = db.session.query(Post).filter(Post.pid==pid).first()
            results = post_dict(post)
            if post.uid != g.uid:
                results["replies"] = None
    except:
        return jsonify({"err" : 1})
    return jsonify({"err" : 1})

@server_api.route('/api/replies')
def get_replies():
    try:
        replies = db.session.query(Reply).join(Post).filter(Post.uid == g.uid).all()
        return jsonify(replies_dict(replies))
    except:
        return jsonify({"err" : 1})

@server_api.route('/api/reply')
def get_reply():
    return jsonify({"err" : 1})

# TODO 需要为item指定pid
@server_api.route('/api/publish')
def publish():
    try:
        data = request.json
        new_post = Post(uid = g.uid,title = data["title"],text = data["text"],kind = data["kind"],date = datetime.datetime(time.localtime()))
        db.session.add(new_post)
        # db.session.commit()
        new_items = []
        for item in data["items"]:
            new_items.append(Item(name = item["name"],text = item["text"],price = item['price'],category = item["category"]))
        db.session.add_all(new_items)
        db.session.commit()
        return jsonify({"err" : 0})
    except:
        return jsonify({"err" : 1}) 

@server_api.route('/api/comment')
def reply():
    try:
        data = request.json
        pid = data['pid']
        items = db.session.query(Item).filter(Item.pid == pid).all()
        items = [item.iid for item in items]
        for item in data['items'].keys():
            if item not in items:
                raise
        new_reply = Reply(text = data['text'],pid = pid,items = json.dump(data['items']))
        return jsonify({"err" : 0})
    except:
        return jsonify({"err" : 1})

@server_api.route('/api/editpost')
def editpost():
    return jsonify({"err" : 1})


@server_api.before_request
def hello():
    t = request.headers.get('Authorization')
    if t != "":
        try:
            nt,info = auth.update_token(t)
            g.uid = info.get("uid")
            g.name = info.get("name")
            if nt!="":
                g.token = nt
            else:
                g.token = t
        except:
            return jsonify({"err": 1})
    else:
        return jsonify({"err": 1})

@server_api.after_request
def bye(response:Response):
    if g.get("token") is not None:
        response.headers['Authorization'] = g.tokens