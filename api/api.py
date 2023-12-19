from typing import Dict
from flask import Blueprint, session, request,g,Response,jsonify
import json
from sqlalchemy import select,or_
from api import auth
from conduit.database import db
from conduit.models import User,Post,Item,Reply,Favorite,Goods,Complaint,Ban
from api.utils import *
import datetime
from conduit.extensions import client
from flask_cors import cross_origin

POST_OPEN = 1
POST_CLOSE = 2
ITEM_OPEN = 1
ITEM_CLOSE = 2
FAV_YES = 1
FAV_NO = 2
COM_UNREAD = 1
COM_YES = 2
COM_NO = 3

CATAGORIES = {
    "daily":"生活用品",
    "book": "书籍",
    "electronic": "电子产品"
}

server_api = Blueprint('api_data', __name__)
@server_api.route('/api/personal',methods = ["POST","GET"])
def get_user_data():
    try:
        user_id = request.args.get("uid", default=g.uid) # 传过来的是字符串
        user_id = int(user_id)
        if user_id<1:
            user_id = g.uid

        if request.method == "GET":
            result = db.session.query(User).filter(User.uid == user_id).first()
            if result is None:
                raise
            return jsonify(user_dict(result))
        else: # "POST"
            result = db.session.query(User).filter(User.uid == user_id).first()
            if result is None:
                raise
            # update
            data = request.json

            if data.get("phone") is not None:
                result.phone = data["phone"]
            if data.get("email") is not None:
                result.email = data["email"]
            if data.get("signature") is not None:
                result.signature = data["signature"]
            if data.get("wx") is not None:
                result.wx = data["wx"]
            if data.get("qq") is not None:
                result.qq = data["qq"]
            if data.get("userName") is not None:
                result.name = data['userName']

            db.session.commit()
            return jsonify({"err" : 0})
    except Exception as e:
        return jsonify({"err" : 1})


@server_api.route('/api/posts',methods = ["POST"])
def get_posts():
    try:
            data = request.json
            kind:int = data.get("kind")
            keywords = data.get("keywords")
            # category = data.get("category")
            category = None
            num = data.get("num")
            start = data.get("start")
            posts = db.session.query(Post, User.name).join(Post, Post.uid == User.uid).filter(Post.kind == kind).filter(Post.status == POST_OPEN)
            if category!=None:
                items = db.session.query(Item).filter(Item.category == category).filter(Item.status == ITEM_OPEN).all()
                pids = []
                for item in items:
                    pids.append(item.__dict__["pid"])
                posts = posts.filter(Post.pid.in_(pids))
            for keyword in keywords:
                # 这里f"{keyword}"会报错，可能跟编码有关系 
                posts = posts.filter(or_(Post.text.like("%{}%".format(keyword)),Post.search.like("%{}%".format(keyword))))
            results = posts.order_by(Post.pid.desc()).limit(num).offset(start).all()
            results = posts_user_dict(results)
            for result in results:
                result["items"] = []
                items = db.session.query(Item).filter(Item.pid == result["pid"]).all()
                for item in items:
                    result["items"].append(item.name)
            return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"err" : 1})

@server_api.route('/api/myposts',methods = ["POST"])
def get_my_posts():
    try:
        data = request.json
        num = data.get("num")
        start = data.get("start")
        posts = db.session.query(Post, User.name).join(Post, Post.uid == User.uid).filter(Post.uid == g.uid)
        results = posts.order_by(Post.pid.desc()).limit(num).offset(start).all()
        results = posts_user_dict(results)
        for result in results:
            result["items"] = []
            items = db.session.query(Item).filter(Item.pid == result["pid"]).all()
            for item in items:
                result["items"].append(item.name)
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"err" : 1})

@server_api.route('/api/post')
def get_post():
    try:
        pid = request.args.get("pid")
        post = db.session.query(Post).filter(Post.pid==pid).first()
        if post is None : raise
        items_result = []
        items = db.session.query(Item).filter(Item.pid == pid).all()
        replies = db.session.query(Reply).filter(Reply.pid == pid).all()
        favorite = db.session.query(Favorite).filter(Favorite.uid == g.uid,Favorite.pid == pid).first()
        want_cnt={}
        want_price = {}
        results_replies = replies_dict(replies)
        postUsername = db.session.query(User.name).filter(User.uid == post.uid).first()[0]
        for item in items:
            want_cnt[str(item.iid)] = 0
            want_price[str(item.iid)] = {}
            items_result.append(item_dict(item))
        for reply in results_replies:
            reply_items = reply['items']
            username = db.session.query(User.name).filter(User.uid == reply['uid']).first()[0]
            reply["userName"] = username
            # reply: { ... }
            # reply_items: [{iid: price}, ...]
            for item in reply_items:
                item_name = db.session.query(Item).filter(Item.iid == item["iid"]).first().name
                want_cnt[str(item["iid"])]+=1
                want_price[str(item["iid"])][username] = item["price"]
                item["name"] = item_name
        results = post_dict(post)
        results["own"] = post.uid == g.uid
        if post.uid != g.uid:
            new_replies = []
            for reply in results_replies:
                if reply["uid"] == g.uid:
                    new_replies.append(reply)
            results["replies"] = new_replies
        else:
            results["replies"] = results_replies
        results["is_favorite"] = favorite is not None        
        # results["want_cnt"] = want_cnt
        results["items"] = items_result
        results['userName'] = postUsername
        # if g.uid != post.uid:
        #     results["want_price"] = {}
        # results["want_price"] = want_price
        for item in items_result:
            item["want_cnt"] = want_cnt[str(item["iid"])]
            item["want_price"] = want_price[str(item["iid"])]
        return jsonify(results)
    except Exception as e:
        return jsonify({"err" : 1})

@server_api.route('/api/replies')
def get_replies_by_user():
    try:
        replies = db.session.query(Reply).join(Post).filter(Post.uid == g.uid).all()
        replies = replies_dict(replies)
        for reply in replies:
            username = db.session.query(User.name).filter(User.uid == reply['uid']).first()[0]
            reply["userName"] = username
            post = db.session.query(Post).filter(Post.pid == reply["pid"]).first()
            reply["post"] = post.title+"。"+post.text
            for item in reply["items"]:
                item_name = db.session.query(Item).filter(Item.iid == item["iid"]).first().name
                item["name"] = item_name
        return jsonify(replies)
    except Exception as e:
        return jsonify({"err" : 1})
    
@server_api.route('/api/post/replies')
def get_replies_by_post():
    pid = request.args.get("pid")
    try:
        replies = db.session.query(Reply).join(Post).filter(Post.pid == pid).all()
        replies = replies_dict(replies)
        for reply in replies:
            username = db.session.query(User.name).filter(User.uid == reply['uid']).first()[0]
            reply["userName"] = username
        return jsonify(replies)
    except Exception as e:
        return jsonify({"err" : 1})
    
@server_api.route('/api/reply')
def get_reply():
    return jsonify({"err" : 1})

# TODO 需要为item指定pid
@server_api.route('/api/publish',methods = ["POST"])
def publish(): 
    try:
        ban_info = db.session.query(Ban).filter(Ban.uid == g.uid).order_by(Ban.date.desc()).first()
        if ban_info is not None:
            if ban_info.end > datetime.datetime.now():
                return jsonify({"err" : 2})
        data = request.json
        pics = data["pictures"]
        pics_urls = [] # 上传到minio的url
        new_items = []
        for pic in pics:
            pics_urls.append(upload_to_minio(pic["picture"],POST_PICS_BKT))
        pics_urls = json.dumps(pics_urls)
        if data.get("location") == None:
            data["location"] = ""
        search = data["title"]+data["location"]
        for item in data["items"]:
            category = CATAGORIES.get(item["category"],"")
            search+=item["name"]+item["description"]+category
            if '.' not in item['price']:
                item['price'] += "00"
                item['price'] = int(item['price'])
            else:
                temp = item['price'].split(".")
                if len(temp[1])==1:
                    temp[1]+='0'
                if len(temp[1])>2:
                    temp[1] = temp[1][:2]
                item['price'] = int(temp[0]+temp[1])
        new_post = Post(uid = g.uid,title = data["title"],text = data["text"],kind = data["kind"],date = datetime.datetime.now(),pics = pics_urls,location = data["location"],search = search)
        db.session.add(new_post)
        db.session.commit()
        for item in data["items"]:
            new_items.append(Item(name = item["name"],pid = new_post.pid,text = item["description"],price = item['price'],category = item["category"]))
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
        pics = data["pictures"]
        pics_urls = [] # 上传到minio的url
        for pic in pics:
            pics_urls.append(upload_to_minio(pic["picture"],REPLY_PICS_BKT))
        pics_urls = json.dumps(pics_urls)
        items = db.session.query(Item).filter(Item.pid == pid).all()
        items = [item.iid for item in items]
        # for item in data['items'].keys():
        #     if int(item) not in items:
        #         return jsonify({"err" : 1})
        for item in data['items']:
            if item["iid"] not in items:
                return jsonify({"err" : 1})

        new_reply = Reply(uid = g.uid, text = data['text'],pid = pid,items = json.dumps(data['items']),date = datetime.datetime.now(), pics = pics_urls)
        db.session.add(new_reply)
        db.session.commit()
        return jsonify({"err" : 0})
    except Exception as e:
        return jsonify({"err" : 1})

@server_api.route('/api/editpost',methods = ["POST"])
def editpost():
    try:
        data = request.json
        pid = data['pid']
        modified_items = data["items"]  # 对象列表
        status = data.get("status")
        if status == None:
            status = POST_OPEN
        post = db.session.query(Post).filter(Post.pid==pid).first()
        if post.status == POST_CLOSE:
            raise
        if status == POST_CLOSE:
            post = db.session.query(Post).filter(Post.pid==pid).update({Post.status:POST_CLOSE,Post.search:""})
            db.session.commit()
            return jsonify({"err" : 0})
        items = db.session.query(Item)
        for item in modified_items:
            items.filter(Item.iid == item['iid']).update({Item.status :item['status']})
            db.session.commit()
        return jsonify({"err" : 0})
    except Exception as e:
        return jsonify({"err" : 1})

### favorite
@server_api.route("/api/editfavorite",methods = ["POST"])
def editfav():
    try:
        data = request.json
        fav = data["fav"]
        if fav == FAV_YES:
            # 加入收藏
            pid = data['pid']
            post = db.session.query(Post).filter(Post.pid==pid).first()
            if post is None:
                return jsonify({"err" : 1})
            new_fav = Favorite(uid = g.uid, pid = post.pid,date = datetime.datetime.now())
            db.session.add(new_fav)
            db.session.commit()
        if fav == FAV_NO:
            # 取消收藏
            pid = data['pid']
            favor = db.session.query(Favorite).filter(Favorite.pid == pid).first()
            db.session.delete(favor)
            db.session.commit()
        return jsonify({"err" : 0})
    except Exception as e:
        return jsonify({"err" : 1})
@server_api.route("/api/getgoodsinfo",methods=["GET"])
def getgoodsinfo():
    try:
        barcode = request.args.get("barcode", default=None)
        if barcode is None: raise
        barcode = barcode.strip()
        # search in db
        goodsinfo = db.session.query(Goods).filter(Goods.barcode==barcode).first()
        if goodsinfo is not None:
            gdict = goods_dict(goodsinfo)
            gdict["err"] = 0
            return jsonify(gdict)
        if (barcode.startswith('978') or barcode.startswith('979')) and len(barcode) == 13:
            # isbn
            result = getbyisbn(barcode)
            if(result["err"] == 0):
                newgoods = Goods(name = result["name"], text = result["text"], category = result["category"], barcode =barcode)
                db.session.add(newgoods)
                db.session.commit()
                return jsonify(result)
            else: return jsonify(result)
        else:
            result = getbygoodscode(barcode)
            if(result["err"] == 0):
                newgoods = Goods(name = result["name"], text = result["text"], category = result["category"], barcode = barcode)
                db.session.add(newgoods)
                db.session.commit()
                return jsonify(result)
            else: return jsonify(result)

        
    except Exception as e:
        print(e)
        return jsonify({"err" : 1}) 

@server_api.route("/api/favorite",methods = ["POST"])
# 根据用户id获取收藏的帖子
def getfavor():
    try:
        data = request.json
        favorites = db.session.query(Favorite).filter(Favorite.uid == g.uid).all()
        pids = [favorite.pid for favorite in favorites]
        num = data.get("num")
        start = data.get("start")
        posts = db.session.query(Post, User.name).join(Post, Post.uid == User.uid).filter(Post.status == POST_OPEN).filter(Post.pid.in_(pids))  
        results = posts.order_by(Post.pid.desc()).limit(num).offset(start).all()
        results = posts_user_dict(results)
        for result in results:
            result["items"] = []
            items = db.session.query(Item).filter(Item.pid == result["pid"]).all()
            for item in items:
                result["items"].append(item.name)
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"err" : 1})
    # try:
    #     uid = g.uid
    #     favorites = db.session.query(Favorite).filter(Favorite.uid == uid).all()
    #     pids = [favorite.pid for favorite in favorites]
    #     posts = db.session.query(Post).filter(Post.pid.in_(pids)).all()
    #     return jsonify(posts_dict(posts))
    # except Exception as e:
    #     return jsonify({"err" : 1})

@server_api.route("/api/report",methods=["POST"])
def report():
    try:
        data = request.json
        new_report = Complaint(uid = g.uid, text = data['text'],pid = data['pid'],date = datetime.datetime.now(),status =COM_UNREAD)
        db.session.add(new_report)
        db.session.commit()
        return jsonify({"err" : 0})
    except Exception as e:
        print(e)
        return jsonify({"err" : 1})

### picture
# from conduit.extensions import client, uploadpic
# @server_api.route("/api/postpic",methods = ["POST"])
# def postpic():
#     try:
#         data = request.json
#         bucket_name = data['kind']
#         for (picname, picdata) in data["data"]:
#             uploadpic(picname, picdata, bucket_name)
#         return jsonify({"err" : 0})
#     except Exception as e:
#         return jsonify({"err" : 1})
# cross origin

@cross_origin(headers=["Content-Type", "Authorization"])
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
            return jsonify({"err": 2})
    else:
        return jsonify({"err": 2})
from conduit.logger import logger
@server_api.after_request
def bye(response):
    # logger.info(request.get_data())
    if g.get("token") != None:
        response.headers['Authorization'] = g.get("token")
    return response
