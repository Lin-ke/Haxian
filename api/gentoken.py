from flask import Blueprint, session, request,g,Response,jsonify
import json
from api import auth
token_api = Blueprint('token_api', __name__)
import requests
def get_wlid_hw(code) -> (bool, str):
    with open("./saved/access_token.txt", "r") as f:
        access_token = f.read()
    headers = {
        'Content-Type': 'application/json',
        'x-wlk-Authorization': access_token
    }
    url = "https://open.welink.huaweicloud.com/api/auth/v2/userid?code={}".format(code)
    r = dict(json.loads(requests.get(url, headers=headers).text))
    if r.get('errorcode') is not None:
        return False, r.get('errormessage', "unknown error")
    if r.get('code', "1") != "0":
        return False, r.get('message', "unknown error")
    return True, r['userId']

@token_api.route('/api/getTokenByCode') 
def get_token_by_code():
    # Because the *code* changes per call, we don't save it.
    code = request.headers.get('Authorization')
    
    if code == "":
        return jsonify({"err": 1, "message" : "provide code"})
    

    result, info = get_wlid_hw(code)
    if not result:
        return jsonify({"err": 1, "message" : info})
    
    # db select uid and name
    #####

    ####
    return jsonify(
        {"err": 0,
        "authorization":auth.gen_token(info, "hw")})
