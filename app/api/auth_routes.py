from app.models import User, db
from app.forms import LoginForm
from app.forms import SignUpForm
from app.utility import signup_status
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user

auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return jsonify({'errors': {'message': 'Unauthorized'}}), 401


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)
        return jsonify(user.to_dict())
    return jsonify(form.errors), 400


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return jsonify({'message': 'User logged out'})


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password']
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify(user.to_dict()), 201

    http_status = signup_status(form.errors)
    return jsonify(form.errors), http_status


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return jsonify({'errors': {'message': 'Unauthorized'}}), 401
