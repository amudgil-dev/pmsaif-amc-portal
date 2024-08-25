from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user,logout_user
from app.helpers.helper_util import enforceAuthz
from app.helpers.queries import checkEntitlements, getUserByUserId
from app.models.models import Session, UserRole
from app.extensions import db
from datetime import datetime, timedelta
import uuid

class AuthHelper:
    @staticmethod
    def check_session_and_authorize(func):
        print('check_session_and_authorize()')
        print(f"func = {func}")
        @wraps(func)
        def decorated_view(*args, **kwargs):
            print(f" check_session_and_authorize() decorated_view func= {func} , args= {args} and kwargs = {kwargs}")

            
                
            print(f"current_user.id = {current_user.id}")
            print(f"current user = {current_user.is_authenticated}")            
            if not current_user.is_authenticated:
                print(' current_user.is_authenticated is not authenticated, sending to login ')
                return redirect(url_for('auth.login'))
            
            
            
            print('checking user_session from the sessions db')
            session = Session.query.filter_by(user_id=current_user.id).first()
            print(f"current_user.id) : {current_user.id}")
            if not session or session.expiry < datetime.utcnow():
                # current_user.logout()
                logout_user()  # Use Flask-Login's logout_user() function
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect(url_for('auth.login'))
            
            
                        # Check if 'pmsid' is in the kwargs
            if 'pms_id' in kwargs:
                pms_id = kwargs['pms_id']
                print(f"pmsid is passed - pmsid = {pms_id}")
                if not enforceEntitlements(current_user.id,pms_id):
                    print('AuthZ Failed and redirecting')
                    return redirect(url_for('pms.pmslist'))
                
            # else:
            #      print(f"pmsid is NOT in kwarks  - pmsid = {kwargs['pms_id']}")
            
            # Check if 'pmsid' is in the args (assuming it's the first argument)
            # elif args and len(args) > 0 and isinstance(args[0], (int, str)) and str(args[0]).isdigit():
            #     print("pmsid is passed as a positional argument")
            
            # # Check the function name
            # if func.__name__ == 'pmslist':
            #     print('FUNCTION IS PMSLIST !!!!!')
            # else:
            #     print(f"FUNCTION IS NOT PMSLIST !!!!! {func.__name__} and {type(func)}")
                

  
            
            return func(*args, **kwargs)
        return decorated_view

    @staticmethod
    def create_session(user):
        print(f"create_session({user.id})")
        session_id = str(uuid.uuid4())
        AuthHelper.delete_session(user.id)
        session = Session(user_id=user.id, session_id=session_id, expiry=datetime.utcnow() + timedelta(hours=1))
        # print(session)
        db.session.add(session)
        db.session.commit()

    @staticmethod
    def delete_session(user_id):
        print(f"delete_session({user_id})")
        # session = Session.query.filter_by(user_id=user_id).first()
        sessions = Session.query.filter_by(user_id=user_id).all()
        print(f"Found {len(sessions)} sessions for user_id {user_id}")
        if sessions:
            for session in sessions:
                db.session.delete(session)
            db.session.commit()
            print(f'Deleted {len(sessions)} old sessions for user_id {user_id}')


def enforceEntitlements(user_id,pms_id):
    print(f"enforceEntitlements( {user_id, pms_id} ) ") 
    
    user = getUserByUserId(user_id)
    
    if user is None:
        return False
    
  
    admin_role_id = UserRole.query.filter_by(name="ADMIN").first().id
    
    # Admins are entitled to access all PMSs
    print(f" user = {user}")
    if user.userrole_id == admin_role_id:
        return True
    
    # If the role is Submitter (any other than Admin) check that the user can only access the PMS belong to their AMC
            
    authz = checkEntitlements(user_id,pms_id)
    if not authz:
        print('You are not authorised to access the PMS you requested, please contat PMSAIF Administrator')
        flash('You are not authorised to access the PMS you requested, please contat PMSAIF Administrator or login with other account!', 'danger')
        return False
    
    return True