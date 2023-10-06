from flask import Blueprint, session, request,g,Response,jsonify
import json
from sqlalchemy import select
from api import auth
from conduit.database import db
from conduit.models import User
from conduit.logger import logger
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


 
# @server_api.before_request
# def hello():
#     t = request.headers.get('Authorization')
#     if t != "":
#         try:
#             nt = auth.update_token(t)
#             if nt!="":
#                 g.token = nt
#             else:
#                 g.token = t
#         except:
#             return jsonify({"err": 1})
#     else:
#         return jsonify({"err": 1})

# @server_api.after_request
# def bye(response:Response):
#     if g.get("token") is not None:
#         response.headers['Authorization'] = g.token