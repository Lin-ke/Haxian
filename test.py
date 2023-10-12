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
        "code" : "96CE5A7FD1F8C508C43DF7FE611004D9AC3C75C57738AF0DB2E0D6E63BC0C0255C6DB1CD14FD9EED2947C74F9A11CBB8"
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


get_token_test()