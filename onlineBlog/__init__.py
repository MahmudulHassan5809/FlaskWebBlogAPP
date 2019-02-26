import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)



##################DataBase Setup#####################

basedir = os.path.abspath(os.path.dirname(__file__))

# Settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# Variables
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#######################################################


##################Login Setup#####################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.lonin_view = 'users.login'
#######################################################

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from onlineBlog.core.views import core
from onlineBlog.error_pages.handlers import error_pages
from onlineBlog.posts.views import posts
from onlineBlog.users.views import users


app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(posts)
app.register_blueprint(users)
