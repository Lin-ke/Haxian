from typing import List
from conduit.models import User,Post,Item,Reply
import json
from minio import Minio
from hashlib import sha256
import io
minio_conf = {
    'endpoint': '0.0.0.0:9000',
    'access_key': 'admin',
    'secret_key': '123456',
    'secure': False
}
REPLY_PICS_BKT = ""
POST_PICS_BKT = ""
IMAGE_MIME = "image/jpeg"


def posts_dict(posts: List[Post])->dict:
    ret = []
    for p in posts:
        temp =p.__dict__
        ret.append(temp)
    return ret

def post_dict(post:Post)->dict:
    temp = post.__dict__
    temp.pop('_sa_instance_state')
    return temp

def replies_dict(replies: List[Reply])->dict:
    temp = []
    for r in replies:
        t = r.__dict__
        t.pop('_sa_instance_state')
        t["items"] = json.loads(t["items"])
        temp.append(t)
    return temp

def reply_dict(reply: Reply)->dict:
    temp = reply.__dict__
    return temp

def upload_to_minio(obj:bytes,bucket:str) -> str:
    client = Minio(**minio_conf)
    name = sha256(obj).hexdigest()
    obj_stream = io.BytesIO(obj)
    client.put_object(bucket_name=bucket, object_name=name,
                       data=obj_stream,
                       content_type=IMAGE_MIME)
    return name