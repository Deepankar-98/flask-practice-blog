from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = '4224303c1bac94a0e9c38ee7b3d3885e'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
crypt = Bcrypt(app)
login_manager = LoginManager(app)

# On trying to open restricted pages its gets redirected to
#  the "login()" function which loads the login page
login_manager.login_view = "login"
# To decorate the message displayed on trying to access restricted url
login_manager.login_message_category = "info"

# Note even thought we have converted the floask application from
# module to package, we still have to watch for circular imports
from flask_app import routes