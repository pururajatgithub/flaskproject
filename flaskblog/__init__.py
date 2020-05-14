
import os
import smtplib
from flask import Flask, Blueprint
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager


#app configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = '79d9541193ace695fa61c51bf6825023'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']  = 'smtp.gmail.com'
app.config['MAIL_PORT']  = 587
app.config['MAIL_USE_TLS']  = True
app.config['MAIL_USERNAME']  = os.environ.get('USE')
app.config['MAIL_PASSWORD']  = os.environ.get('PASS')
mail = Mail(app)
from flaskblog.users.routes import users  
from flaskblog.posts.routes import posts 
from flaskblog.main.routes import main 


app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)