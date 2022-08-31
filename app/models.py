from datetime import datetime, timedelta
from email.policy import default
from itertools import product
from tokenize import String

from flask import current_app

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, login_manager, app

from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin, current_user

from sqlalchemy import ForeignKey





@login_manager.user_loader 
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.Text())
    admin_role = db.Column(db.Integer(), default=0)
    phone = db.Column(db.Text(), unique= True)
    city = db.Column(db.Text())
    
    
    def get_reset_token(self, expires_sec=1800): #expires_sec - время через сколько перестанет действовать токен
        s = Serializer(app.config['SECRET_KEY'], expires_sec) #генерация токена по secret_key текущего пользователя и добавляет время жизни
        return s.dumps({'user_id': self.id}).decode('utf-8') #делает переменную как токен, через которыц можно узнать id пользователя и в котором будет время жизни.
    
    
    @staticmethod
    def verify_reset_token(token): #берем токен
        s = Serializer(app.config['SECRET_KEY']) #берем ключ
        try:
            user_id = s.loads(token)['user_id'] #из токена берем id пользователя.
        except:
            return None #если токен истек то возращается None
        
        return User.query.get(user_id) #функция вернет пользователя, которому принадлежит токен.
    
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.create_password()
    
    def create_password(self):
        self.password = generate_password_hash(self.password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return "<id: {},username: {}, email: {}>".format(self.id, self.username, self.email)  


    
class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False) 
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text())
    size = db.Column(db.String(150))
    link = db.Column(db.Text, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    
    
    def __init__(self, *args, **kwargs):
        super(Products, self).__init__(*args, **kwargs)         
        self.link = str(self.name).replace(' ','-')
        
    def __repr__(self):
        return 'USER id: {}, name {}'.format(self.id, self.name)
    


class Brand(db.Model):  #jordan
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return 'BRAND id: {}, name {}'.format(self.id, self.name)


class Category(db.Model): # Jordan 1, jordan 2
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand_name = db.Column(db.String, db.ForeignKey('brand.name'))
    
    
    def __repr__(self):
        return 'CATEGORY id: {}, name {}'.format(self.id, self.name)
    


class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False) 
    phone = db.Column(db.Text(), nullable=False)
    city = db.Column(db.Text(), nullable=False)
    address = db.Column(db.String(100), nullable=False) 
    index = db.Column(db.Integer(), nullable=False)
    delivery = db.Column(db.String(100)) 
    pay = db.Column(db.String(100))
    products = db.Column(db.String())