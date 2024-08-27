"""Authentication blueprint for handling user authentication and password reset."""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.helpers.helper_util import generate_resetlink, email_resetlink, isAdmin
from app.models.models import User
from app.forms.forms import ResetPasswordForm, ResetRequestForm, SigninForm
from app.helpers.auth_helper import AuthHelper
from app.helpers.logging_helper import warning, error, log_function_call
from app.extensions import login_manager, db

bp_auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

@bp_auth.route('/login', methods=['GET', 'POST'])
@log_function_call
def login():
    """Handle user login."""
    form = SigninForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password_hash.data.strip()
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            warning(f"Failed login attempt for user: {email}")
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user)
        AuthHelper.create_session(user)
        user.user_id = current_user.id
        flash(f"Welcome back, {user.fname} {user.lname}!", 'success')

        if isAdmin(user.userrole_id):
            return redirect('/admin')
        
        return redirect('/pmslist')

    return render_template("form_login.html",
                           page_heading="Login",
                           email=None,
                           form=form)

@bp_auth.route('/logout')
@login_required
@log_function_call
def logout():
    """Handle user logout."""
    AuthHelper.delete_session(current_user.id)
    logout_user()
    return redirect(url_for('home.index'))

@bp_auth.errorhandler(Exception)
def handle_exception(e):
    """Handle exceptions in the auth blueprint."""
    error(f"Unhandled exception in auth blueprint: {str(e)}")
    return "An error occurred", 500

@bp_auth.route('/resetreq', methods=['GET', 'POST'])
def user_reset_req():
    """Handle password reset requests."""
    try:
        AuthHelper.delete_session(current_user.id)
    except AttributeError:
        pass

    logout_user()
    form = ResetRequestForm()

    if form.validate_on_submit():
        email = form.email.data.strip()
        user = User.query.filter_by(email=email).first()

        if user:
            reset_link = generate_resetlink(user)
            email_resetlink(reset_link, email)
            flash("Reset link is sent which is valid for 5 mins!", 'success')
            return redirect("/logout")

        flash("If your mail is registered, you will receive a password reset link, else consider registering!", 'warning')
        return redirect("/register")

    return render_template("form_resetreq.html",
                           page_heading="Reset Password Request",
                           email=None,
                           form=form)

@bp_auth.route('/resetpwd/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset."""
    logout_user()
    user = User.verify_token(token)

    if user is None:
        flash("Invalid or expired token, try again!", 'warning')
        return redirect("/resetreq")

    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = form.password_hash.data.strip()
        user.set_password(new_password)
        db.session.commit()
        flash("Password changed successfully!", 'success')
        return redirect("/login")

    return render_template("form_createpwd.html",
                           form=form,
                           token=token,
                           page_heading="Create New Password...")
    