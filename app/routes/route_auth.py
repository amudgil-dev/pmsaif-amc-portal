from flask import Blueprint, render_template, redirect, url_for, flash,current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import User
from app.forms.forms import SigninForm
from app.helpers.auth_helper import AuthHelper
from app.helpers.logging_helper import debug, info, warning, error, critical, log_exception, log_function_call
from app.extensions import login_manager

bp_auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp_auth.route('/login', methods=['GET', 'POST'])
@log_function_call
def login():
    print(' in login()')
    if current_user.is_authenticated:
        print('redirecting to txn')
        return redirect(url_for('txn.transactions'))
    
    print('before form')
    form = SigninForm()
    if form.validate_on_submit():
        print(' after validation')
        
        email = form.email.data.strip()
        password = form.password_hash.data.strip()
        
        # user = User1.query.filter_by(username=form.email.data).first()
        user = User.query.filter_by(email=email).first()
        
        print(' after db lookup')
        if user is None or not user.check_password(password):
            warning(f"Failed login attempt for user: {email}")
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        AuthHelper.create_session(user)
        
        # admin_role, user_id, user_role = isAdmin(session)
        

        print(f"current_user.id = {current_user.id}")
        print(f"current user = {current_user.is_authenticated}")
        user.user_id = current_user.id
        
        # user.user_role = user_role
        flash("Welcome back, " + user.fname + " " + user.lname + " !", 'success')
        print('session created and now sending to /pmslist')
        return redirect('/pmslist')
          
        # return redirect(url_for('txn.transactions'))
    # info('Successful login for user: %s', user.username)
    # return render_template('login.html', form=form)
    print(" in GET render form_login.html")
    email = None    
    form.email.data = '' 
    form.password_hash.data = ''        
    return render_template("form_login.html", 
                        page_heading="Login",
                        email= email,
                        form= form)
    

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