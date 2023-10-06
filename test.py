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
def token_test():
    import requests
    import json
    headers = {"Authorization":
                "CAB2EFD701E59C5AC34703B9A5BEDE4955643FA2030040F944D503EE6AFA5032FEFCD38964F1482703DCBEEDBF5A83C1"}
    r = requests.get('http://localhost:5000/api/getTokenByCode',headers=headers)
    print(r.text)
def get_data_test():
    import requests
    import json
    r = requests.get('http://localhost:5000/api/getdata')
    print(r.text)
get_data_test()