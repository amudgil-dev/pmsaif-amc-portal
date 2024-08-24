from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user,logout_user
from app.models.models import Session
from app.extensions import db
from datetime import datetime, timedelta
import uuid

class AuthHelper:
    @staticmethod
    def check_session_and_authorize(func):
        print('check_session_and_authorize()')
        @wraps(func)
        def decorated_view(*args, **kwargs):
            print(' check_session_and_authorize() decorated_view')
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
        