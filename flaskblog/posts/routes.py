from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import post
from flaskblog.posts.forms import PostForm

posts= Blueprint('posts_blue', __name__)







@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        Post= post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(Post)
        db.session.commit()
        flash('Posted!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New  Post', legend='New Post', form=form)








@posts.route("/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_posts(post_id):
    posts=post.query.get_or_404(post_id)
    if posts.author != current_user:
        abort(403)
    db.session.delete(posts)
    db.session.commit()
    flash('Posted Updated Successfully!', 'success')
    return redirect(url_for('main.home'))






@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    posts = post.query.get_or_404(post_id)
    if posts.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        posts.title = form.title.data
        posts.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = posts.title
        form.content.data = posts.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')



@posts.route("/posts/<int:post_id>")
def posts(post_id):
    posts=post.query.get_or_404(post_id)
    return render_template('posts.html', title=posts.title, posts=posts)