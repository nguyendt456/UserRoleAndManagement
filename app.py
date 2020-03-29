from flask import Flask, render_template, request, Response, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin
from sqlalchemy.exc import IntegrityError
import json 

app = Flask(__name__, static_url_path='/static')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = "phuongquyen"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['DEBUG'] = True

class User(db.Model, UserMixin):
    def __init__(self, user):
        self.username = user['username']
        self.password = user['password']
        self.email = user['email']
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

@login_manager.user_loader
def load_user(user_id):
    usid = User.query.get(user_id)
    print(usid)
    return usid

@app.route("/",methods = ['GET','POST'])
def index():
    if current_user.is_authenticated:
        return render_template("index.html", users = User.query.all())
    else:
        if request.is_json:
            userinp = request.get_json()
            userdata = User.query.filter_by(username = userinp['username']).first()
            if userdata != None:
                if userinp['password'] == userdata.password:
                    login_user(userdata)
                    return Response("Logged In",200)
                else:
                    return Response("Wrong password",200)
            else:
                return Response("Wrong username !",200)
        else:
            return render_template("login.html")

@app.route("/register", methods = ['GET','POST'])
def reg():
    if request.is_json:
        try:
            newuser = request.get_json()
            regdata = User(newuser)
            db.session.add(regdata)
            role = Role.query.filter_by(name = newuser['role']).first()
            role.roler.append(regdata)
            db.session.commit()
            return Response("Account added !",200)
        except IntegrityError:
            db.session.rollback()
            return Response("Username already exists !",200)
    else:
        return render_template('register.html')
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run("0.0.0.0",80)

