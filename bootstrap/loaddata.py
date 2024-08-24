from app import db
from app.models.models import User, Transaction
import random
from datetime import datetime, timedelta

def load_sample_data():
    db.create_all()

    # Create sample users
    user1 = User(username='debit_user', user_type='debit')
    user1.set_password('password')
    user2 = User(username='credit_user', user_type='credit')
    user2.set_password('password')

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create sample transactions
    for i in range(20):
        txn = Transaction(
            user_id=user1.id if i % 2 == 0 else user2.id,
            txn_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            txn_amount=random.uniform(10, 1000),
            txn_type='debit' if i % 2 == 0 else 'credit'
        )
        db.session.add(txn)

    db.session.commit()
    print("Sample data loaded successfully.")