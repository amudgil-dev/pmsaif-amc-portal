from datetime import datetime
import threading
from modules.db_schema import TxnLog, TxnType, db
from flask import current_app

def log_txn(msgType, log_desc, user_id, created_at=None):
    print('log_txn()')
    
    # if created_at is None:
    #     created_at = datetime.now()
    
    # # Get the current application context
    # ctx = current_app.app_context()
    
    # newThread = threading.Thread(target=log_txn_async, args=[ctx, msgType, log_desc, user_id, created_at])
    # newThread.start()

    return True

def log_txn_async(app_context, msgType, log_desc, user_id, created_at):
    print('log_txn_async()')
    
    with app_context:
        try:
            print("1")
            print(msgType)
            txn_type = db.session.query(TxnType).filter(TxnType.name == msgType).first().id

            log = TxnLog(txntype_id=txn_type, log_desc=log_desc, user_id=user_id, created_at=created_at)
            db.session.add(log)
            db.session.commit()
        except Exception as ex:
            print(f"Error in log_txn_async: {ex}")
            db.session.rollback()

            log_unknown_txn(log_desc=log_desc, user_id=user_id, created_at=created_at)
    
    return True

def log_unknown_txn(log_desc, user_id, created_at):
    with current_app.app_context():
        try:
            unknown_type = db.session.query(TxnType).filter(TxnType.name == "UNKNOWN").first().id
        
            log = TxnLog(txntype_id=unknown_type, log_desc=log_desc, user_id=user_id, created_at=created_at)    

            db.session.add(log)
            db.session.commit()
        except Exception as ex:
            print(f"Error in log_unknown_txn: {ex}")
            db.session.rollback()
    
    return True