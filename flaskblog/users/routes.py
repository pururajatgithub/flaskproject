  
from flask import  render_template, redirect, request, abort
from flask import flash
from flaskblog import app
from flaskblog import bcrypt, mail
from flask import url_for
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateForm, ResetPasswordForm, ResetForm
from flaskblog.users.utils import save_picture, send_email
from flaskblog.models import user, post
from flaskblog import db
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
                                   
from flaskblog.users.utils import save_picture, send_email

from  flask  import Blueprint

users= Blueprint('users_blue', __name__)

@users.route('/register', methods=['GET','Post'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User=user(username=form.username.data, email=form.email.data, phone=form.phone.data, password=hashed_password)
        db.session.add(User)
        db.session.commit()
        return redirect(url_for('users.login'))
        flash('Acount Created successfully!', 'success')
    return render_template('register.html', title='Register',form=form)




@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        User = user.query.filter_by(email=form.email.data).first()
        if User and bcrypt.check_password_hash(User.password, form.password.data):
            login_user(User, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout" )
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET','POST'] )
@login_required
def account():
    image_file=url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file,)

@users.route("/updateprofile", methods=['GET','POST'] )
@login_required
def updateprofile():
    form= UpdateForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.phone=form.phone.data
        db.session.commit()
        flash('Your Account has been updated')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    return render_template('update.html', title='Update Profile', form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    User = user.query.filter_by(username=username).first_or_404()
    posts = post.query.filter_by(author=User).order_by(post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, title='Blogs', user=User)



@users.route("/reset",methods=['GET','POST'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=ResetForm()
    if form.validate_on_submit():
        User=user.query.filter_by(email=form.email.data).first()
        send_email(User)
        flash('Check your Email to reset password ')
        return redirect(url_for('users.login'))
    return render_template('reset.html',title='Reset Password', form=form)

@users.route("/reset/<token>", methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    User=user.verify_reset_token(token)
    if User is None:
        flash('Expired!', 'warning' )
        return redirect(url_for('users.reset'))
    form= ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.password = hashed_password
        db.session.commit()
        return redirect(url_for('users.login'))
        flash('Your Password has been updated sucessfully!', 'success')
    return render_template('reset_pasword.html',title='Reset Password', form=form)