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
def db_add_goods():
    from autoapp import app
    from conduit.models import Goods
    from conduit.database import db
    with app.app_context():
        goods_new = Goods(name='农夫山泉550ml瓶装水', text="我们不生产水，我们只是大自然的搬运工",category="drink",barcode="6921168509256")    
        db.session.add(goods_new)
        db.session.commit()

def get_data_test():
    import requests
    import json
    r = requests.get('http://localhost:5000/api/getdata')
    print(r.text)
def get_token_test():
    import requests,json
    args = {
        "code" : "EDF3CEF705B1917F7C058CB37B2FDDD495ABE94DFF9790D3777AE3BEB815DD09DE3C7E5F2ECEED212BE8D1C709789F72"
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
def get_douban():
    import requests
    head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.7 (KHTML, like Gecko) Chrome/20.0.1099.0 Safari/536.7 QQBrowser/6.14.15493.201",
    "Accept-Language": "en-US,en;q=0.9",
    }
    isbn = "9787303271672"
    t = requests.get("https://book.douban.com/isbn/{}/".format(isbn),headers = head)
    from lxml import etree
    
    print(t.text)

db_add_goods()