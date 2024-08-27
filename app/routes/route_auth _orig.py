from flask import Blueprint, render_template, redirect, url_for, flash,current_app,request
from flask_login import login_user, logout_user, login_required, current_user
from app.helpers.helper_util import generate_resetlink,email_resetlink, isAdmin
from app.models.models import User
from app.forms.forms import ResetPasswordForm, ResetRequestForm, SigninForm
from app.helpers.auth_helper import AuthHelper
from app.helpers.logging_helper import debug, info, warning, error, critical, log_exception, log_function_call
from app.extensions import login_manager, db

bp_auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp_auth.route('/login', methods=['GET', 'POST'])
@log_function_call
def login():
    print(' in login()')
    # if current_user.is_authenticated:
    #     print('redirecting to /pmslist')
    #     return redirect(url_for('pms.pmslist'))
    
    print('before form')
    form = SigninForm()
    if form.validate_on_submit():
        # print(' after validation')
        
        email = form.email.data.strip()
        password = form.password_hash.data.strip()
        
        # user = User1.query.filter_by(username=form.email.data).first()
        user = User.query.filter_by(email=email).first()
        
        # print(f"after db lookup user = {user.userrole_id}")
        if user is None or not user.check_password(password):
            warning(f"Failed login attempt for user: {email}")
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        AuthHelper.create_session(user)
        
        # admin_role, user_id, user_role = isAdmin(session)
        

        # print(f"current_user.id = {current_user.id}")
        # print(f"current user = {current_user.is_authenticated}")
        user.user_id = current_user.id
        
        # user.user_role = user_role
        flash("Welcome back, " + user.fname + " " + user.lname + " !", 'success')
        
        # print(f" user = {user}")
        
        if  isAdmin(user.userrole_id):
            # print('session created role is admin and now sending to /admin')
            return redirect('/admin')
        else:
            
            # print('session created and role is submitter now sending to /pmslist')
            return redirect('/pmslist')
          
        # return redirect(url_for('txn.transactions'))
    # info('Successful login for user: %s', user.username)
    # return render_template('login.html', form=form)
    # print(" in GET render form_login.html")
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
    AuthHelper.delete_session(current_user.id)
    logout_user()
    return redirect(url_for('home.index'))



# Error handling example
@bp_auth.errorhandler(Exception)
def handle_exception(e):
    error(f"Unhandled exception in auth blueprint: {str(e)}")
    # You might want to render an error template or return an error response here
    return "An error occurred", 500



# create reset request
@bp_auth.route('/resetreq', methods=['GET','POST'])
def user_reset_req():
    # print('in user_reset_req()')
    try:
        AuthHelper.delete_session(current_user.id)
        print(' session deleted')
    except:
        pass

    logout_user()
    # print('user logged out')
  # if current_user.is_authenticated:
  #    logout_user()
    # print(' before form')
    email = None
    form = ResetRequestForm()

    if request.method=="POST":
        if form.validate_on_submit():
            email = form.email.data.strip()
            user = User.query.filter_by(email=email).first()

            # user is found, means the email is registered,
            if user:
                reset_link = generate_resetlink (user)
                # print(f"reset_link = {reset_link} ")
                email_resetlink(reset_link, email)
                flash("Reset link is sent which is valid for 5 mins!", 'success')
                return redirect("/logout")
            else:
                # print("user is none")
                flash(" If your mail is registered, you will receive an passsword reset link, else consider registering !", 'warning')
                return redirect("/register")
        else:
            flash(form.errors, 'danger')
            return render_template("form_resetreq.html", 
                                    page_heading="Reset Password Request",
                                    email= email,
                                    form= form)

    if request.method=="GET":
        # return render_template("register_user.html")
        form.email.data = ''   
        return render_template("form_resetreq.html", 
                                email= email,
                                form= form, 
                                page_heading="Reset Password Request ...",
                                Title = ""
                                )
                            
  
####### validating the link when customer clicks on it and allowing creation of new passsword afterwards! ############

@bp_auth.route('/resetpwd/<token>', methods=['GET','POST'])
def reset_password(token):
    # print('in reset_password()')
    logout_user()

    # print(f" token = {token}")  
    # print(request.method)
    user = User.verify_token(token)
    if user is None:
        # print("user is none")
        flash("Invalid or expired token, try again!", 'warning')
        return redirect("/resetreq")
    
    # print('user is not None')
    if request.method=="POST":
        # print('in reset_password() post ')
        form = ResetPasswordForm()
        if form.validate_on_submit():
            new_password = form.password_hash.data.strip() 
            # new_passsword_hash = generate_password_hash(new_password)
            # user.password_hash = new_passsword_hash
            user.set_password(new_password)
            db.session.commit()
            # print('user password changed!')
            flash("Password changed successfully !", 'success')
            return redirect("/login")

    if request.method=="GET":
        # print(' method is GET')
        form = ResetPasswordForm()
        return render_template("form_createpwd.html",
                            form=form, 
                            token=token,
                            page_heading="Create New Password ...",)