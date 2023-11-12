# pinning_lab/auth/views.py

# external imports
from flask import Blueprint, render_template, \
    redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask_login import login_user, logout_user, \
    login_required, current_user

# Local imports
from pinning_lab.database.models import Users
from pinning_lab import db

# Logging
import logging
logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """ Login GET method """
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """ Login POST method """
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/signup')
def signup():
    """ Sign up GET method """
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    """ Sign up POST method """
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = Users.query.filter_by(email=email).first()
    # if a user is found, we want to redirect back to signup page so user can try again
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = Users()
    new_user.email = email
    new_user.username = username
    new_user.password = generate_password_hash(
        password, method='sha256')
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    """ Logout GET method """
    logout_user()
    return redirect(url_for('home.index'))


@auth.route('/profile')
@login_required
def profile():
    user = Users.query.filter_by(username=current_user.username).first()
    return render_template(
        'auth/profile.html',
        user=user
    )
