from flask import Blueprint, session, request,g,Response,jsonify
import json
from api import auth
token_api = Blueprint('token_api', __name__)
from conduit.database import db
from conduit.models import User
import requests
from conduit.logger import logger
from flask_cors import cross_origin
def get_wlid_hw(code) -> (bool, str):
    with open("./saved/access_token.txt", "r") as f:
        access_token = f.read()
    headers = {
        'Content-Type': 'application/json',
        'x-wlk-Authorization': access_token
    }
    url = "https://open.welink.huaweicloud.com/api/auth/v2/userid?code={}".format(code)
    r = dict(json.loads(requests.get(url, headers=headers).text))
    logger.info(r)
    if r.get('errorcode') is not None:
        return False, r.get('errorMessage', "unknown error")
    if r.get('code', "1") != "0":
        return False, r.get('message', "unknown error")
    return True, r['userId']
@cross_origin(headers=["Content-Type", "Authorization"])
@token_api.route('/api/login') 
def login():
    if request.method == "GET":
        # Because the *code* changes per call, we don't save it.
        code = request.args.get("code",default="",type=str)
    if code == "":
        return jsonify({"err": 1, "message" : "provide code"})
    result, wlid = get_wlid_hw(code)
    print(result)
    if not result:
        return jsonify({"err": 1, "message" : "Unknown"})
    # db select uid and name
    result = db.session.query(User).filter(User.wlid == wlid).first()
    if result == None:
        db.session.add(User(wlid = wlid,name = wlid.split("_")[0]))
        db.session.commit()
        result = db.session.query(User).filter(User.wlid == wlid).first()
    return jsonify(
        {"err": 0,
        "token":auth.gen_token(result.uid, result.name)})
