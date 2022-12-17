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
    db.Column('user_id', db.String(50), db.ForeignKey('user.id')),
    db.Column('recipe_id', db.String(50), db.ForeignKey('user.id'))
)



class User(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable = False, unique=True)
    password = db.Column(db.String(150), nullable = True)

    saved = db.relationship("SavedRecipes", backref='user', lazy=True)
    saved_recipe = db.relationship('User',
        primaryjoin = (recipes.c.user_id==id),
        secondaryjoin = (recipes.c.recipe_id==id),
        secondary = recipes,
        backref = db.backref('user_recipes', lazy='dynamic'),
        lazy = 'dynamic'
        )

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
    
    def get_id(self):
        return self.id

    def set_token(self, length):
        return secrets.token_hex(length)

    def updateUserInfo(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password



class SavedRecipes(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)
    preptime = db.Column(db.String(30), nullable=True)
    cooktime = db.Column(db.String(30), nullable=True)
    servings = db.Column(db.String(30), nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, rid, title, img_url, user_id):
        self.rid = rid
        self.title = title
        self.img_url = img_url
        # self.preptime = preptime
        # self.cooktime = cooktime
        # self.servings = servings
        # self.instructions = instructions
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
