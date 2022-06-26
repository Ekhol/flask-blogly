"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from importlib_metadata import method_cache
from models import db, connect_db, User

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return redirect("/users")


@app.route('/users')
def user_list():

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users=users)


@app.route('/users/new', methods=["GET"])
def new_user():
    return render_template("users/new.html")


@app.route('/users/new', methods=["POST"])
def new_user_submit():

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/details.html", user=user)


@app.route('/user/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route('/user/<int:user_id>/edit', methods=["POST"])
def update_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
