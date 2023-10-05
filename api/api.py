from flask import Blueprint, session, request,g,Response,jsonify
import json
from api import auth
server_api = Blueprint('api_data', __name__)
 
 
@server_api.route('/api/getdata')
def get_data():
    result, info = auth.verify_token(g.get("token"))
    if result:
        user_id = info["id"]
        user_name = info["name"]
    # continue...
    return '{"user_name": "libai", "user_pwd": "123456"}'   #json响应


 
@server_api.before_request
def hello():
    t = request.headers.get('Authorization')
    if t != "":
        try:
            nt = auth.update_token(t)
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
        response.headers['Authorization'] = g.token