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

def getAllUser():
    return backend.storeprocess._getAllUserInfo()

def getUserByID(id):
    try:
        return backend.storeprocess._getUserbyID(id)
    except NotFind:
        return None

def getUserByAccount(accnum):
    try:
        return backend.storeprocess._getUserbyAccount(accnum)
    except NotFind:
        return None

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

def getAllAccount():
    return backend.storeprocess._getAllAccountInfo('Saving') + backend.storeprocess._getAllAccountInfo('Checking')

def getAccountType(accnum):
    return backend.storeprocess._getAccountType(accnum)

def getAccountByID(id):
    return backend.storeprocess._getAccountByID('Saving', id) + backend.storeprocess._getAccountByID('Checking', id)

def getAccountBySub(subname):
    return backend.storeprocess._getAllAccountBySubName('Saving', subname) + backend.storeprocess._getAllAccountBySubName('Checking', subname)

def addUser2Account(id, accnum):
    backend.storeprocess._addUser2Account(id, accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
        raise UnknownError
        
# def dataStatistic():
