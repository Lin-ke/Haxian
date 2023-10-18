from typing import List
from conduit.models import User,Post,Item,Reply
import json
from minio import Minio
from hashlib import sha256
import io
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
    temp.pop("name")
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
    return temp
def upload_to_minio(obj:bytes,bucket:str) -> str:
    name = sha256(obj).hexdigest()
    obj_stream = io.BytesIO(obj)
    result= client.put_object(bucket_name=bucket, object_name=name,
                       data=obj_stream, length=len(obj))
    return bucket+ "/" + name