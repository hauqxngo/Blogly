"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask.globals import request
from werkzeug.utils import redirect
from models import db, connect_db, User
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
def list_users():
    """Show list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)

@app.route('/new', methods=['GET'])    
def new_user_form():
    """Show new user form"""
    return render_template('form.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')
    # or to show user detail page
    # return redirect(f'/{new_user.id}')

@app.route('/<int:user_id>')
def show_user(user_id):
    """Show user detail page"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit a user form"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Edit current user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deleting the current user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
