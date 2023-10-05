from models import *
def db_test():
    from app import app,db

    with app.app_context():
        for i in range(10):
            new_user = User(name='John{}'.format(str(i)), email='john@example.com')
            db.session.add(new_user)
        db.session.commit()
        for i in range(10):
            user = User.query.filter_by(name='John{}'.format(str(i))).first()
            print(user)
            db.session.delete(user)
def token_test():
    import requests
    import json
    headers = {"Authorization":
                "CAB2EFD701E59C5AC34703B9A5BEDE4955643FA2030040F944D503EE6AFA5032FEFCD38964F1482703DCBEEDBF5A83C1"}
    r = requests.get('http://localhost:5000/api/getTokenByCode',headers=headers)
    print(r.text)

token_test()