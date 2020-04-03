from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = "friendzone:))"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['DEBUG'] = True

from routes import *

if __name__ == "__main__":
    app.run("0.0.0.0",8080)
