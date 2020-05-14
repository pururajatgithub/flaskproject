from flask import render_template, request, Blueprint
from flaskblog.models import post
from  flask  import Blueprint

main= Blueprint('main_blue', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = post.query.order_by(post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='Blogs')


 
@main.route('/about')
def about():                         
    return render_template('about.html', title='About Us')



