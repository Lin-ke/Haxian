import jwt
import time

HEADERS = {
  "alg": "HS256",
  "typ": "JWT"
}
SALT = "kbugvsvzvbqapqrk"
EXPIRE_TIME = 72000

def gen_token(uid,name)->str:
  exp = int(time.time() + EXPIRE_TIME)
  payload = {
  "uid":uid ,
  "name": name,
  "exp": exp
  }
  token = jwt.encode(payload=payload, key=SALT, algorithm='HS256', headers=HEADERS)
  return token
  # info = jwt.decode(token, SALT, algorithms=["HS256"])

def verify_token(token):
  try:
      info = jwt.decode(token, SALT, algorithms=["HS256"])
      return True,info
  except:
     return False,{}
  
def update_token(old_token)->tuple[str, dict]:
  result,info = verify_token(old_token)
  if result:
    if time.time()-info['exp'] > EXPIRE_TIME//2:
      new_token = gen_token(info["uid"],info["name"])
      return new_token,info
    else:
        return "",info
  else:
    raise