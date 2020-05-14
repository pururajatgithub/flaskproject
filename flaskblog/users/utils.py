import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture():
    pass


def send_email(User):

    token = User.get_reset_token()
    msg =  Message('Reset Passowrd', sender='noreply@blog.com', recipients=[User.email])
    
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_password',token=token, _external=True)}
If you did not makethis  request  then ignore this message
'''


    mail.send(msg)
