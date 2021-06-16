import backend.storeprocess
from sqlalchemy import exc
from backend.exceptions import *

def importSqlfile(filepath):
    backend.storeprocess._importSqlfile(filepath)

def createUser(info):
    backend.storeprocess._createUser(info)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()

def alterUser(id, newinfo):
    backend.storeprocess._alterUser(id, newinfo)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()

def delUser(id):
    backend.storeprocess._delUser(id)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()

def createAccount(acctype, info):
    Transactions = backend.storeprocess._createAccount(acctype, info)
    try:
        Transactions.commit()
        backend.storeprocess.db_session.commit()
    except Exception:
        Transactions.rollback()
        backend.storeprocess.db_session.rollback()
        raise Exception

def delAccount(accnum):
    backend.storeprocess._delAccount(accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
