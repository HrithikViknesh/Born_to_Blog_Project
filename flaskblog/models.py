from datetime import datetime
from flaskblog import db
from flask import current_app
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
#  for tokenizing secrets

# Tokenizer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Login Manager
from flaskblog import login_manager
from flask_login import UserMixin


# decorator fn to get username from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# We'll use sqlite db for dev

# here in sqlite classes are tables in db

# Table to store user credentials


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email = db.Column(db.String(length=120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # need not be unique
    password = db.Column(db.String(60), nullable=False)  # need not be unique

    # Define relationship to be used as foreign key in Posts
    posts = db.relationship('Post', backref='author', lazy=True)

    # IMP: Here Post is in Pascal Case since here 'Post' refers to the Post class

    # When querying user table, posts is not actually a column in the table, rather the post from Post table is fetched
    # by providing backref we can use the statement post.author to get the user object of that post
    # lazy controls when is db loaded

    # Provide Token for password reset
    def provide_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)

        return s.dumps({'user_id': self.id}).decode('utf-8')  # self refers to user object

    # Static method to Verify token during password reset
    ## Static because no modifications made to (or) any use made out of  User object(self)
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):  # dunder method to specify how printing out a user object should look like
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# We define a one to many relation from User to Post, so that one user can author more than 1 post


# Table to store use posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Pass function itself as parameter
    content = db.Column(db.Text, nullable=False)
    # foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes_by = db.Column(db.String(length=40), nullable=True, default='')
    likes = db.Column(db.Integer, default=0)
    # liked_by = db.Column(MutableList.as_mutable(PickleType), default=[])
    #liked_by = db.Column(db.String(length=200),default = '')
    # IMP: But here we use snake case for 'user' since we are referring to the table db model and not the User class
    # Table( also columns) names are inherently converted to lower case

    def __repr__(self):  # dunder method to specify how printing out a user object should look like
        return f"User('{self.title}', '{self.date_posted}')"
