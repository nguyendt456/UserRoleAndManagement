from init import db, login_manager, app
from models import User, UserRole, Role
from flask import Flask, render_template, request, Response, url_for, redirect
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from string import ascii_letters, digits
import json


def Validate(form):
    error = []
    if (set(form['username']).difference(ascii_letters + digits)):
        error.append('Username must not contain special characters!')
    if (len(form['username']) <= 4 and len(form['username']) >= 20):
        error.append('Username must from 5 to 19 character!')
    if (len(form['password']) <= 4 and len(form['password']) >= 20):
        error.append('Password must from 5 to 19 character!')
    try:
        form['email'].index('@')
    except:
        error.append('Please enter valid email address!')
    return error


@login_manager.user_loader
def load_user(user_id):
    usid = User.query.get(user_id)
    print(usid)
    return usid


@app.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        print("ok")
        return render_template("base.j2", users=User.query.all(), body='dashboard')
    elif (bool(request.form.to_dict()) == True):
        user = request.form
        userfromdatabase = User.query.filter_by(
            username=user['username']).first()
        if userfromdatabase != None:
            if user['password'] == userfromdatabase.password:
                login_user(userfromdatabase)
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
        return redirect(url_for('index'))
    return render_template('base.j2', body='login')


@app.route("/register", methods=['GET', 'POST'])
def reg():
    error = []
    form = request.form
    if bool(form.to_dict()) == True:
        error = Validate(form)
        if error == []:
            user = User(username=form['username'],
                        password=form['password'], email=form['email'])
            print(form.to_dict())
            role = Role.query.filter_by(name=form.get('role')).first()
            role.roler.append(user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('base.j2', errors=error, body='register')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
