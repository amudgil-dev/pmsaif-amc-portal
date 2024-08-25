from contextlib import contextmanager
from app import db

@contextmanager
def safe_transaction():
    """
    A context manager to handle database transactions safely.
    It will commit if no exception occurs, and rollback if an exception is raised.
    """
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise