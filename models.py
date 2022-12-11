from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets
from sqlalchemy.orm import relationship

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

recipes = db.Table('recipes',
    db.Column('user_id', db.String(50), db.ForeignKey('user.uid')),
    db.Column('recipe_id', db.String(50), db.ForeignKey('user.uid'))
)


class User(db.Model, UserMixin):
    uid = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable = False, unique=True)
    password = db.Column(db.String(150), nullable = True, default = '')
    # g_auth_verify = db.Column(db.Boolean, default = False)
    # token = db.Column(db.String, default = '', unique = True )
    

    saved = db.relationship("SavedRecipes", backref='user', lazy=True)
    saved_recipe = db.relationship('User',
        primaryjoin = (recipes.c.user_id==uid),
        secondaryjoin = (recipes.c.recipe_id==uid),
        secondary = recipes,
        backref = db.backref('user_recipes', lazy='dynamic'),
        lazy = 'dynamic'
        )


    def __init__(self, uid, email,username, password=''):
        self.uid = uid
        self.username = username
        self.password = password
        self.email = email
        # self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    # def set_id(self):
    #     return str(uuid.uuid4())
    
    # def set_password(self, password):
    #     self.pw_hash = generate_password_hash(password)
    #     return self.pw_hash
    
    def updateUserInfo(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'User {self.email} has been added to the database'


class SavedRecipes(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)
    preptime = db.Column(db.String(30), nullable=True)
    cooktime = db.Column(db.String(30), nullable=True)
    servings = db.Column(db.String(30), nullable=True)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('user.uid'), nullable=False)

    def __init__(self, rid, title, img_url, preptime, cooktime, servings, instructions, user_id):
        self.rid = rid
        self.title = title
        self.img_url = img_url
        self.preptime = preptime
        self.cooktime = cooktime
        self.servings = servings
        self.instructions = instructions
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
