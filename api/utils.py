from typing import List
from conduit.models import User,Post,Item,Reply

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
        temp.append(t)
    return temp

def reply_dict(reply: Reply)->dict:
    temp = reply.__dict__
    return temp