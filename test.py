def db_test():
    from autoapp import app
    from conduit.models import User
    from conduit.database import db
        

    with app.app_context():
        for i in range(20):
            new_user = User(name='John{}'.format(str(i)), email='john@example.com', wild='123456789{}'.format(str(i)))
            db.session.add(new_user)
            db.session.commit()
        for i in range(10):
            user = User.query.filter_by(name='John{}'.format(str(i))).first()
            db.session.delete(user)
            db.session.commit()

def get_data_test():
    import requests
    import json
    r = requests.get('http://localhost:5000/api/getdata')
    print(r.text)
def get_token_test():
    import requests,json
    args = {
        "code" : "1FD242211E8F72E543166C95EA0A78C47F07D64AF526734D5A5F9F9280B29B55929D281E2B31C5AA0AEEB68E02CF28EE"
    }
    r = requests.get('http://localhost:14535/api/login',params=args)
    print(r.headers)
    print(r.text)

def db_droop_all():
    from autoapp import app
    from conduit.models import User
    from conduit.database import db
    with app.app_context():
        db.drop_all()

def test_minio():
    from minio import Minio
    import os, datetime
    client = Minio(
	# endpoint指定的是你Minio的远程IP及端口
    # localhost:39.107.83.124
	endpoint = "localhost:9000",
	# accesskey指定的是你的Minio服务器访问key
	# 默认值为minioadmin
	access_key= "123",
	# secret_key指定的是你登录时需要用的key，类似密码
	# 默认值也是minioadmin
	secret_key= "12345678",
	# secure指定是否以安全模式创建Minio连接
	# 建议为False
	secure= False)
    year,m =datetime.datetime.now().strftime("%Y-%m").split("-")
    with open("./pics/xt.jpg", "rb") as f:
        bytes_len = os.path.getsize("./pics/xt.jpg")
        client.put_object("test","{}/{}/xt.jpg".format(year,m),f,bytes_len)
    url = client.presigned_get_object("test", "xt.jpg")
    print(url)
read_policy = "{\n" +\
    "    \"Version\": \"2012-10-17\",\n" +\
    "    \"Statement\": [\n" +\
    "        {\n" +\
    "            \"Sid\":\"PublicRead\",\n" +\
    "            \"Effect\": \"Allow\",\n" +\
    "            \"Principal\": \"*\",\n" +\
    "            \"Action\": [\n" +\
    "                \"s3:GetBucketLocation\",\n" +\
    "                \"s3:GetObject\"\n" +\
    "            ],\n" +\
    "            \"Resource\": [\n" +\
    "                \"arn:aws:s3:::*\"\n" +\
    "            ]\n" +\
    "        }\n" +\
    "    ]\n" +\
    "}"
def init_minio():
    from conduit.extensions import client
    for i in ['reply','post','item','user']:
        if client.bucket_exists(i):
            #删除
            client.remove_bucket(i)
        client.make_bucket(i)
        #策略
        client.set_bucket_policy(i,read_policy)
    



get_token_test()