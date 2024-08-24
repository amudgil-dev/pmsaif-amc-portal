from flask import Blueprint, render_template, redirect, url_for, flash,current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import User
from app.forms.forms import LoginForm
from app.helpers.auth_helper import AuthHelper
from app.helpers.logging_helper import debug, info, warning, error, critical, log_exception, log_function_call

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/login', methods=['GET', 'POST'])
@log_function_call
def login():
    print(' in login()')
    if current_user.is_authenticated:
        return redirect(url_for('txn.transactions'))
    
    print('before form')
    form = LoginForm()
    if form.validate_on_submit():
        print(' after validation')
        print(form.username.data,form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        print(' after db lookup')
        if user is None or not user.check_password(form.password.data):
            warning(f"Failed login attempt for user: {form.username.data}")
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        AuthHelper.create_session(user)
        return redirect(url_for('txn.transactions'))
    # info('Successful login for user: %s', user.username)
    return render_template('login.html', form=form)

@bp_auth.route('/logout')
@login_required
@log_function_call
def logout():
    AuthHelper.delete_session(current_user)
    logout_user()
    return redirect(url_for('home.index'))

# Error handling example
@bp_auth.errorhandler(Exception)
def handle_exception(e):
    error(f"Unhandled exception in auth blueprint: {str(e)}")
    # You might want to render an error template or return an error response here
    return "An error occurred", 500