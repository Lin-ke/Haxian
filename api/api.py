from typing import Dict
from flask import Blueprint, session, request,g,Response,jsonify
import json
from sqlalchemy import select
from api import auth
from conduit.database import db
from conduit.models import User,Post,Item,Reply,Favorite
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

@server_api.route('/api/posts',methods = ["POST"])
def get_posts():
    try:
            data = request.json
            kind:int = data.get("kind")
            keywords = data.get("keywords")
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

@server_api.route('/api/post')
def get_post():
    try:
        pid = request.args.get("pid")
        post = db.session.query(Post).filter(Post.pid==pid).first()
        items = db.session.query(Item).filter(Item.pid == pid).all()
        replies = db.session.query(Reply).filter(Reply.pid == pid).all()
        favorite = db.session.query(Favorite).filter(Favorite.uid == g.uid).filter(Favorite.pid == pid).first()
        want_cnt={}
        want_price = {}
        results_replies = replies_dict(replies)
        for item in items:
            want_cnt[item.iid] = 0
            want_price[item.iid] = {}
        for reply in results_replies:
            reply_items = json.loads(reply['items'])
            for item in reply_items.keys():
                want_cnt[item]+=1
                want_price[item][reply['uid']] = reply_items[item]
        results = post_dict(post)
        if post.uid != g.uid:
            results["replies"] = []
        else:
            results["replies"] = results_replies
        results["is_favorite"] = favorite is not None        
        results["want_cnt"] = want_cnt
        results["want_price"] = want_price
        return jsonify(results)
    except Exception as e:
        return jsonify({"err" : 1})

@server_api.route('/api/user/replies')
def get_replies_by_user():
    try:
        replies = db.session.query(Reply).join(Post).filter(Post.uid == g.uid).all()
        return jsonify(replies_dict(replies))
    except Exception as e:
        return jsonify({"err" : 1})
    
@server_api.route('/api/post/replies')
def get_replies_by_post():
    pid = request.args.get("pid")
    try:
        replies = db.session.query(Reply).join(Post).filter(Post.pid == pid).all()
        return jsonify(replies_dict(replies))
    except Exception as e:
        return jsonify({"err" : 1})
    
@server_api.route('/api/reply')
def get_reply():
    return jsonify({"err" : 1})

# TODO 需要为item指定pid
@server_api.route('/api/publish',methods = ["POST"])
def publish():
    try:
        data = request.json
        new_post = Post(uid = g.uid,title = data["title"],text = data["text"],kind = data["kind"],date = datetime.datetime.now())
        db.session.add(new_post)
        db.session.commit()
        new_items = []
        for item in data["items"]:
            new_items.append(Item(name = item["name"],pid = new_post.pid,text = item["text"],price = item['price'],category = item["category"]))
        db.session.add_all(new_items)
        db.session.commit()
        return jsonify({"err" : 0})
    except Exception as e:
        return jsonify({"err" : 1}) 

@server_api.route('/api/comment',methods = ["POST"])
def reply():
    try:
        data = request.json
        pid = data['pid']
        items = db.session.query(Item).filter(Item.pid == pid).all()
        items = [item.iid for item in items]
        for item in data['items'].keys():
            if int(item) not in items:
                return jsonify({"err" : 1})
        new_reply = Reply(uid = g.uid, text = data['text'],pid = pid,items = json.dumps(data['items']),date = datetime.datetime.now())
        db.session.add(new_reply)
        db.session.commit()
        return jsonify({"err" : 0})
    except Exception as e:
        return jsonify({"err" : 1})

@server_api.route('/api/editpost')
def editpost():
    try:
        data = request.json
        pid = data['pid']
        modified_items = data["items"]  # 键值对
        status = data["status"]
        post = db.session.query(Post).filter(Post.pid==pid).first()
        if post.status == 2:
            raise
        if status == 2:
            post = db.session.query(Post).filter(Post.pid==pid).update({Post.status:2})
            db.session.commit()
            return jsonify({"err" : 0})
        items = db.session.query(Item)
        for iid,s in modified_items.items():
            items.filter(Item.iid == iid).update({Item.status :s})
            db.session.commit()
    except Exception as e:
        return jsonify({"err" : 1})

### favorite
@server_api.route("/api/editfavorite")
def editfav():
    try:
        data = request.json
        status = data["status"]
        if status == 1:
            # 加入收藏
            pid = data['pid']
            post = db.session.query(Post).filter(Post.pid==pid).first()
            if post is None:
                return jsonify({"err" : 1})
            new_fav = Favorite(uid = g.uid, pid = post.pid,date = datetime.datetime.now())
            db.session.add(new_fav)
            db.session.commit()
        if status == 2:
            # 取消收藏
            pid = data['pid']
            favor = db.session.query(Favorite).filter(Favorite.pid == pid).first()
            db.session.delete(favor)
            db.session.commit()
        return jsonify({"err" : 0})
    except Exception as e:
        return jsonify({"err" : 1})
        

###

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
        except Exception as e:
            return jsonify({"err": 1})
    else:
        return jsonify({"err": 1})

@server_api.after_request
def bye(response):
    if g.get("token") != None:
        response.headers['Authorization'] = g.get("token")
    return response