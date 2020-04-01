from init import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(120), unique = False, nullable = False)
    email = db.Column(db.String(120), nullable = False)
    role = db.relationship('Role', secondary = 'user_role', backref = db.backref('roler',lazy = 'dynamic'))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(20), unique = True)

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer(),db.ForeignKey('roles.id'))
