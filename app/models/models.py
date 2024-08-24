from app.extensions import db, login_manager
# ... rest of the code remains the same

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(10))  # 'debit' or 'credit'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    txn_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    txn_amount = db.Column(db.Float, nullable=False)
    txn_type = db.Column(db.String(10), nullable=False)  # 'debit' or 'credit'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))