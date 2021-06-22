import backend.storeprocess
import sqlalchemy
from backend.exceptions import *

def importSqlfile(filepath):
    backend.storeprocess._importSqlfile(filepath)

def getAllWorkerInfo():
    return backend.storeprocess._getAllWorkerInfo()

def createUser(info):
    backend.storeprocess._createUser(info)
    backend.storeprocess._addRelate({
        "ID": info['ID'],
        "WorkerID": info['WorkerID'],
        "Role": info['Role'],
    })
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def alterUser(id, newinfo):
    backend.storeprocess._alterUser(id, newinfo.copy())
    backend.storeprocess._alterRelate({
        "ID": newinfo['ID'],
        "WorkerID": newinfo['WorkerID'],
        "Role": newinfo['Role'],
    })
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def delUser(id):
    backend.storeprocess._delUser(id)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def getUser(info):
    return backend.storeprocess._getUserInfo(info)

def createAccount(acctype, info):
    Transactions = backend.storeprocess._createAccount(acctype, info)
    try:
        Transactions.commit()
    except Exception as e:
        Transactions.rollback()
        raise e

def delAccount(accnum):
    backend.storeprocess._delAccount(accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def alterAccount(accnum, newinfo):
    newinfo['AccNum'] = accnum
    acctype = backend.storeprocess._getAccountType(accnum)
    backend.storeprocess._alterAccount(acctype, accnum, newinfo)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def addUser2Account(ID, accnum):
    backend.storeprocess._addUser2Account(ID, accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def getAllAccount():
    return backend.storeprocess._getAllAccountInfo('Saving') + backend.storeprocess._getAllAccountInfo('Checking')

def getAccountType(accnum):
    return backend.storeprocess._getAccountType(accnum)

def getAccount(info):
    return backend.storeprocess._getAccount(info)

def getAccountByID(id):
    return backend.storeprocess._getAccountByID('Saving', id) + backend.storeprocess._getAccountByID('Checking', id)

def getAccountBySub(subname):
    return backend.storeprocess._getAllAccountBySubName('Saving', subname) + backend.storeprocess._getAllAccountBySubName('Checking', subname)

def addUser2Account(id, accnum):
    backend.storeprocess._addUser2Account(id, accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def createLoan(info, userlist):
    backend.storeprocess._createLoan(info, userlist)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def getAllLoan():
    return backend.storeprocess._getAllLoan()

def getLoanByNum(num):
    return backend.storeprocess._getLoanByLoanNum(num)

def getLoanByID(id):
    return backend.storeprocess._getAllLoanByID(id)

def getPaied4Loan(loannum):
    return backend.storeprocess._getPaiedForLoan(loannum)

def delLoan(loannum):
    backend.storeprocess._delLoan(loannum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def getLoanStatus(loannum):
    return backend.storeprocess._getLoanStatus(loannum)

def getLoan(info):
    return backend.storeprocess._getLoan(info)

def payForLoan(info):
    loaninfo = backend.storeprocess._getLoanByLoanNum(info['LoanNum'])
    info['SubName'] = loaninfo.SubName
    backend.storeprocess._grantLoan(info)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def getAllSub():
    return backend.storeprocess._getAllSubInfo()

def dataStatistic(sublist, starttime, endtime):
    datalist = []
    for sub in sublist:
        checking = backend.storeprocess._getCheckingAccountBySubName(sub, time={"start":starttime,"end":endtime})
        saving = backend.storeprocess._getSavingAccountBySubName(sub, time={"start":starttime,"end":endtime})
        loan = backend.storeprocess._getLoanPaiedBySubName(sub, time={"start":starttime,"end":endtime})
        if len(starttime) and len(endtime):
            checkingnum = sum([account[0].Balance for account in checking])
            savingnum = sum([account[0].Balance for account in saving])
        else:
            checkingnum = sum([account.Balance for account in checking])
            savingnum = sum([account.Balance for account in saving])
        datalist.append({
            "Subbranch": sub,
            "Assets": checkingnum + savingnum - loan,
            "CheckingAssets": checkingnum,
            "SavingAssets": savingnum,
            "SavingAccountNum": len(saving), 
            "CheckingAccountNum":len(checking),
            "LoanAssets": -loan,
        })

    return datalist

def Auth(username, pwd):
    return backend.storeprocess._auth(username, pwd)
    
def addAdmin(username, pwd):
    backend.storeprocess._addAdmin(username, pwd)
    try:
        backend.storeprocess.db_session.commit()
    except Exception as e:
        backend.storeprocess.db_session.rollback()
        raise e

def getAdmin(username):
    return backend.storeprocess._getAdmin(username)