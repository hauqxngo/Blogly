"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask.globals import request
from werkzeug.utils import redirect
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

# Having the Debug Toolbar show redirects explicitly is often useful, but this line below is to turn it off
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('/posts/homepage.html', posts=posts)

# @app.errorhandler(404)
# def page_not_found(e):
#     """Show 404 NOT FOUND page."""
#     return render_template('404.html'), 404

################################################################################
# User route

@app.route('/users')
def list_users():
    """Show list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/list.html', users=users)

@app.route('/users/new', methods=['GET'])    
def new_user_form():
    """Show new user form"""
    return render_template('/users/new.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url' or None]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user detail page"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/details.html', user=user,)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit a user form"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Edit current user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deleting the current user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect('/users')

###############################################################################
# Posts route

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    return render_template('/posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deleting the post."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect('/users')