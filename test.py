from app import app,db
from models import *
with app.app_context():
    for i in range(10):
        new_user = User(name='John{}'.format(str(i)), email='john@example.com')
        db.session.add(new_user)
    db.session.commit()
    for i in range(10):
        user = User.query.filter_by(name='John{}'.format(str(i))).first()
        print(user)
        db.session.delete(user)