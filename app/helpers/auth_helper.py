from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user,logout_user
from app.helpers.helper_util import enforceAuthz
from app.helpers.queries import checkEntitlementsFromDB, getUserByUserId
from app.models.models import Session, UserRole
from app.extensions import db
from datetime import datetime, timedelta
import uuid

class AuthHelper:
    @staticmethod
    def check_session(func):
        # print('check_session()')
        # print(f"func = {func}")
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # print(f" check_session() decorated_view func= {func} , args= {args} and kwargs = {kwargs}")

            # print(f"current_user.id = {current_user.id}")
            # print(f"current user = {current_user.is_authenticated}")            
            if not current_user.is_authenticated:
                # print(' current_user.is_authenticated is not authenticated, sending to login ')
                return redirect(url_for('auth.login'))
            
            # print('checking user_session from the sessions db')
            session = Session.query.filter_by(user_id=current_user.id).first()
            # print(f"current_user.id) : {current_user.id}")
            if not session or session.expiry < datetime.utcnow():
                # current_user.logout()
                logout_user()  # Use Flask-Login's logout_user() function
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect(url_for('auth.login'))
                            
            return func(*args, **kwargs)
        return decorated_view

    @staticmethod
    def check_pms_authorisations(func):
        # print('check_pms_authorisations()')
        # print(f"func = {func}")
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # print(f" check_pms_authorisations() decorated_view func= {func} , args= {args} and kwargs = {kwargs}")

            # Check if 'pmsid' is in the kwargs
            if 'pms_id' in kwargs:
                pms_id = kwargs['pms_id']
                # print(f"pmsid is passed - pmsid = {pms_id}")
                if not enforceSubmitterEntitlements(current_user.id,pms_id):
                    # print('AuthZ Failed and redirecting')
                    flash('You are not authorised to access the PMS you requested, please contat PMSAIF Administrator or login with other account!', 'danger')
                    return redirect(url_for('pms.pmslist'))
                            
            return func(*args, **kwargs)
        return decorated_view
    
    @staticmethod
    def check_admin_authorisations(func):
        # print('check_admin_authorisations()')
        # print(f"func = {func}")
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # print(f" check_admin_authorisations() decorated_view func= {func} , args= {args} and kwargs = {kwargs}")

            if not enforceAdminEntitlements(current_user.id):
                # print('AuthZ Failed and redirecting')
                flash('You are not authorised to access the resource you requested, please contat PMSAIF Administrator or login with other account!', 'danger')
                return redirect(url_for('auth.logout'))
                            
            return func(*args, **kwargs)
        return decorated_view
    
    @staticmethod
    def create_session(user):
        # print(f"create_session({user.id})")
        session_id = str(uuid.uuid4())
        AuthHelper.delete_session(user.id)
        session = Session(user_id=user.id, session_id=session_id, expiry=datetime.utcnow() + timedelta(hours=1))
        # print(session)
        db.session.add(session)
        db.session.commit()

    @staticmethod
    def delete_session(user_id):
        # print(f"delete_session({user_id})")
        # session = Session.query.filter_by(user_id=user_id).first()
        sessions = Session.query.filter_by(user_id=user_id).all()
        # print(f"Found {len(sessions)} sessions for user_id {user_id}")
        if sessions:
            for session in sessions:
                db.session.delete(session)
            db.session.commit()
            # print(f'Deleted {len(sessions)} old sessions for user_id {user_id}')


def enforceSubmitterEntitlements(user_id,pms_id):
    # print(f"enforceSubmitterEntitlements( {user_id, pms_id} ) ") 
    
    user = getUserByUserId(user_id)
    
    if user is None:
        return False
    
    admin_role_id = UserRole.query.filter_by(name="ADMIN").first().id
    
    # print(f"admin_role_id= {admin_role_id} and user.userrole_id = {user.userrole_id} ")
    # print(' checking Admin role')
    
    # Admins are entitled to access all PMSs
    if user.userrole_id == admin_role_id:
        # print(' ADMIN IS TRUE')
        return True
    
    # If the role is Submitter (any other than Admin) check that the user can only access the PMS belong to their AMC
    return checkEntitlementsFromDB(user_id,pms_id)

def enforceAdminEntitlements(user_id):
    # print(f"enforceAdminEntitlements( {user_id} ) ") 
    
    user = getUserByUserId(user_id)
    
    if user is None:
        return False
    
    admin_role_id = UserRole.query.filter_by(name="ADMIN").first().id
    
    # Admins are entitled to access all PMSs
    # print(f" user = {user}")
    if not user.userrole_id == admin_role_id:
        return False
    
    
    return True