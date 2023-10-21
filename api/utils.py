from typing import List
from conduit.models import User,Post,Item,Reply
import json
from minio import Minio
from hashlib import sha256
import io,base64
import numpy as np
from PIL import Image
from conduit.extensions import client
self_host = "http://39.107.83.124:9000"
minio_conf = {
    'endpoint': '0.0.0.0:9000',
    'access_key': 'admin',
    'secret_key': '123456',
    'secure': False
}
REPLY_PICS_BKT = "reply"
POST_PICS_BKT = "post"
TARGET_SIZE = 1024

def posts_dict(posts: List[Post])->dict:
    ret = []
    for p in posts:
        temp = post_dict(p)
        ret.append(temp)
    return ret

def post_dict(post:Post)->dict:
    temp = post.__dict__
    temp.pop('_sa_instance_state')
    temp.pop("search")
    temp["pics"] = json.loads(temp["pics"])
    return temp
def user_dict(user:User)->dict:
    temp = user.__dict__
    temp.pop('_sa_instance_state')
    temp.pop("wlid")
    return temp

def posts_user_dict(posts: List)->dict:
    ret = []
    for p in posts:
        temp = post_user_dict(p)
        ret.append(temp)
    return ret

def post_user_dict(post)->dict:
    temp = post_dict(post[0])
    temp["userName"] = post[1]
    # templist = []
    # for pic in temp["pics"]:
    #     templist.append(pic+".thumbnail")
    # temp["pics"] = templist
    return temp

def replies_dict(replies: List[Reply])->dict:
    temp = []
    for r in replies:
        t = reply_dict(r)
        t["items"] = json.loads(t["items"])
        temp.append(t)
    return temp

def reply_dict(reply: Reply)->dict:
    temp = reply.__dict__
    temp.pop('_sa_instance_state')
    temp["pics"] = json.loads(temp["pics"])
    return temp
def item_dict(item: Item)->dict:
    temp = {}
    temp["iid"] = item.iid
    # temp["pid"] = item.pid
    temp["name"] = item.name
    temp["text"] = item.text
    temp["price"] = str(item.price)[0:-2]+"."+str(item.price)[-2:]
    temp["category"] = item.category
    temp["status"] = item.status
    return temp
def upload_to_minio(obj:str,bucket:str) -> str:
    obj_bytes = obj.encode()
    name = sha256(obj_bytes).hexdigest()
    upload_thumbnail(obj, bucket, name)
    # obj_stream = io.BytesIO(obj_bytes)
    # client.put_object(bucket_name=bucket, object_name=name,
    #                    data=obj_stream, length=len(obj))
    return bucket+ "/" + name

def upload_thumbnail(obj:str, bucket:str,name:str):
    t,real_obj = obj.split(',')
    data = base64.b64decode(real_obj.encode())
    # resize real_obj as image
    img = Image.open(io.BytesIO(data))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    w,h = img.size
    if h >= w:
        RATIO = TARGET_SIZE/h
        if h > TARGET_SIZE:
            w,h = int(w*RATIO), TARGET_SIZE
            img = img.resize((w,h))
    else:
        RATIO = TARGET_SIZE/w
        if w > TARGET_SIZE:
            w,h = TARGET_SIZE, int(h*RATIO)
            img = img.resize((w,h))

    # convert img to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
    img_base64= base64.b64encode(img_bytes)
    img_str = 'data:image/jpg;base64,'.encode()+img_base64
    # client.put_object(bucket_name=bucket, object_name=name+".thumbnail",
    #                    data=io.BytesIO(img_str), length=len(img_str))
    client.put_object(bucket_name=bucket, object_name=name,
                       data=io.BytesIO(img_str), length=len(img_str))
    