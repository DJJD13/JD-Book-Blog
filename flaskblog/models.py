from datetime import datetime
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
# This is deprecated. Change to a different JWS token library like pyjwt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# This decorator is necessary for setting up the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# The UserMixin includes a bunch of necessary login functionality
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    books = db.relationship('Book', backref='poster', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # Sets how we print out the User
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # date_started = db.Column(db.DateTime, default=datetime.utcnow)
    # date_finished = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Book('{self.title}','{self.date_posted}')"
