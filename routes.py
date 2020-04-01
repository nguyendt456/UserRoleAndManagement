from init import db, login_manager, app
from models import User, UserRole, Role
from forms import RegistrationForm
from flask import Flask, render_template, request, Response, url_for,redirect
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError
import json

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
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password.data, email = form.email.data)
        role = Role.query.filter_by(name = form.role.data).first()
        role.roler.append(user)
        db.session.add(user)
        db.session.commit()
        return flash(u'Acount Added')
    return render_template('register.html')
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
