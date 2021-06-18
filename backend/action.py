import backend.storeprocess
import sqlalchemy
from backend.exceptions import *

def importSqlfile(filepath):
    backend.storeprocess._importSqlfile(filepath)

def getAllWorkerInfo():
    return backend.storeprocess._getAllWorkerInfo()

def createUser(info):
    backend.storeprocess._createUser(info)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
        raise UnknownError

def alterUser(id, newinfo):
    backend.storeprocess._alterUser(id, newinfo)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
        raise UnknownError

def delUser(id):
    backend.storeprocess._delUser(id)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
        raise UnknownError

def createAccount(acctype, info):
    Transactions = backend.storeprocess._createAccount(acctype, info)
    try:
        Transactions.commit()
        backend.storeprocess.db_session.commit()
    except Exception:
        Transactions.rollback()
        backend.storeprocess.db_session.rollback()
        raise UnknownError

def delAccount(accnum):
    backend.storeprocess._delAccount(accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
        raise UnknownError

def alterAccount(accnum, newinfo):
    newinfo['AccNum'] = accnum
    acctype = backend.storeprocess._getAccountType(accnum)
    backend.storeprocess._alterAccount(acctype, accnum, newinfo)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
        raise UnknownError

def addUser2Account(ID, accnum):
    backend.storeprocess._addUser2Account(ID, accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
        raise UnknownError

# def dataStatistic():
