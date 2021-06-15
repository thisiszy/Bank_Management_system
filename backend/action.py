from backend.model import *
from backend.exceptions import *
from sqlalchemy import Column, String, create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.database import db_session
from sqlalchemy import exc

# result = session.execute(select(Worker).where(Worker.WorkerAddr.like('Beijing%')))
# print(book)

'''
import sql file to mysqldb by filepath
'''
def importSqlfile(filepath):
    from subprocess import Popen, PIPE
    process = Popen(['mysql', '-u', 'root'],
                    stdout=PIPE, stdin=PIPE)
    cmd = 'use lab3; source ' + filepath + ';'
    output = process.communicate(cmd.encode('utf-8'))[0]

'''
return all workerinfo from Worker table
'''
def getAllWorkerInfo():
    return db_session.query(Worker).all()
    
'''
add a new worker to Worker table
'''
def createWorker(info):
    w = Worker(info)
    db_session.add(w)
    db_session.commit()

'''
return explicit workerinfo from Worker table
input: id(str)
'''
def getWorkerbyID(id):
    t = db_session.query(Worker).filter(Worker.WorkerID == id)
    if t is None:
        raise NotFind
    return t

# '''
# alter worker information
# input: id(str), newinfo(dict)
# '''
# # TODO:员工号修改之后还需要修改
# # Manager Relate Department等表
# def alterWorker(id, newinfo):
#     # w = Worker(newinfo)
#     id = int(id)
#     t = db_session.query(Worker).filter(Worker.WorkerID == id).update(newinfo)
#     db_session.commit()

'''
alter Bank Assets
modify assets of subbranch
SubBranch.SubAssets += change
input: subname(str), change(Float(8))
'''
def alterBankAsset(subname, change):
    b = db_session.query(Subbranch).filter(Subbranch.SubName == subname).first()
    if b is None:
        raise NotFind
    b.SubAssets += change
    db_session.add(b)
    db_session.commit()

'''
add a new user
input: info(dict)
info include ID, Address, ContectName, ContectTel,
ContectEmail, Relationship
'''
def createUser(info):
    # if already have same ID user
    if db_session.query(User).filter(User.ID == info['ID']).first() is not None:
        raise DupId
    # 
    if len(info) < len(User.__table__.columns):
        raise IncompleteData
    p = User(info)
    db_session.add(p)
    db_session.commit()

'''
delete userinfo by id
input: id(str)
'''
def delUser(id):
    if db_session.query(User).filter(User.ID == id).first() is None:
        raise NotFind
    try:
        db_session.query(User).filter(User.ID == id).delete()
    except exec.IntegrityError:
        raise Unmodifiable("Can't delete item with foreign key")
    db_session.commit()

'''
alter user
input: id(str), newinfo(dict)
newinfo include ID, Address, ContectName, ContectTel,
ContectEmail, Relationship
'''
def alterUser(id, newinfo):
    if id != newinfo['id']:
        raise Unmodifiable
    if db_session.query(User).filter(User.ID == id).first() is None:
        raise NotFind
    if len(newinfo) < len(User.__table__.columns):
        raise IncompleteData
    db_session.query(User).filter(User.ID == id).update(newinfo)
    db_session.commit()

'''
return all userinfo from User table
'''
def getAllUserInfo():
    return db_session.query(User).all()

'''
return explicit userinfo from User table
input: id(str)
'''
def getUserbyID(id):
    t = db_session.query(User).filter(User.ID == id)
    if t is None:
        raise NotFind
    return t

'''
add relate between Worker and User
input: info(dict)
info include WorkerID, ID and Role
'''
def addRelate(info):
    if db_session.query(User).filter(User.ID == info['ID']).first() is None:
        raise NotFind("Not find User")
    if db_session.query(Worker).filter(Worker.ID == info['WorkerID']).first() is None:
        raise NotFind("Not find Worker")
    if db_session.query(Relate).filter(Relate.ID == info['ID'], Relate.WorkerID == info['WorkerID']).first() is not None:
        raise DupId
    if len(info) < len(Relate.__table__.columns):
        raise IncompleteData
    db_session.add(Relate(info))
    db_session.commit()

'''
alter relate between Worker and User
input: info(dict)
info include WorkerID, ID and Role
'''
def alterRelate(newinfo):
    if db_session.query(Relate).filter(Relate.ID == newinfo['ID'], Relate.WorkerID == newinfo['WorkerID']).first() is None:
        raise NotFind
    if len(newinfo) < len(Relate.__table__.columns):
        raise IncompleteData
    db_session.query(Relate).filter(Relate.ID == newinfo['ID'], Relate.WorkerID == newinfo['WorkerID']).update(newinfo)
    db_session.commit()

'''
add account
input: acctype(str), managementinfo(dict), accountinfo(dict)
acctype == 'Checking' or 'Saving'
managementinfo include ID, SubName, AccNum
accountinfo include AccNum, Balance, LastAccessTime, OpenDate
'''
def createAccount(acctype, managementinfo, accountinfo):
    if 'LastAccessTime' in accountinfo:
        del accountinfo['LastAccessTime']
    if len(managementinfo) < len(SavingManagement.__table__.columns):
        raise IncompleteData("incomplete management info")
    if managementinfo['AccNum'] != accountinfo['AccNum']:
        raise Unmodifiable('Account number different')
    if acctype == 'Checking':
        if db_session.query(CheckingManagement).filter(CheckingManagement.ID == managementinfo['ID'], CheckingManagement.SubName == managementinfo['SubName']).first() is not None:
            raise DupId('Duplicated Card')
        if db_session.query(Checking).filter(Checking.AccNum == managementinfo['AccNum']).first() is not None:
            raise DupId('Duplicated Account number')
        if len(accountinfo) < len(CheckingManagement.__table__.columns)-1:
            raise IncompleteData("incomplete CheckingManagement info")
        db_session.add(Checking(accountinfo))
        db_session.add(CheckingManagement(managementinfo))
        db_session.commit()
    elif acctype == 'Saving':
        if db_session.query(SavingManagement).filter(SavingManagement.ID == managementinfo['ID'], SavingManagement.SubName == managementinfo['SubName']).first() is not None:
            raise DupId('Duplicated Card')
        if db_session.query(Saving).filter(Saving.AccNum == managementinfo['AccNum']).first() is not None:
            raise DupId('Duplicated Account number')
        if len(accountinfo) < len(SavingManagement.__table__.columns)-1:
            raise IncompleteData("incomplete SavingManagement info")
        db_session.add(Saving(accountinfo))
        db_session.add(SavingManagement(managementinfo))
        db_session.commit()
    else:
        raise UndefindBehaviour
    alterBankAsset(managementinfo['SubName'], float(accountinfo['Balance']))

'''
delete account
input: acctype(str), accnum(str)
acctype == 'Checking' or 'Saving'
'''
def delAccount(acctype, accnum):
    if acctype == 'Checking':
        acc = db_session.query(Checking).filter(Checking.AccNum == accnum)
        if acc.first() is None:
            raise NotFind('Account not find')
        manage = db_session.query(CheckingManagement).filter(CheckingManagement.AccNum == accnum)
        if manage.first() is None:
            raise NotFind('Account management not find')
        alterBankAsset(manage.first().SubName, -acc.first().Balance)
        db_session.query(Account).filter(Account.AccNum == accnum).delete()
        db_session.commit()
    elif acctype == 'Saving':
        acc = db_session.query(Saving).filter(Saving.AccNum == accnum)
        if acc.first() is None:
            raise NotFind
        manage = db_session.query(SavingManagement).filter(SavingManagement.AccNum == accnum)
        if manage.first() is None:
            raise NotFind('Account management not find')
        alterBankAsset(manage.first().SubName, -acc.first().Balance)
        db_session.query(Account).filter(Account.AccNum == accnum).delete()
        db_session.commit()
    else:
        raise UndefindBehaviour

'''
alter accountinfo
input: acctype(str), accnum(str), newinfo(dict)
acctype == 'Checking' or 'Saving'
newinfo include AccNum, Balance, LastAccessTime, OpenDate
'''
def alterAccount(acctype, accnum, newinfo):
    if accnum != newinfo['AccNum']:
        raise Unmodifiable
    if acctype == 'Checking':
        if len(newinfo) < len(Checking.__table__.columns):
            raise IncompleteData
        acc = db_session.query(Checking).filter(Checking.AccNum == accnum)
        if acc.first() is None:
            raise NotFind('Account not find')
        manage = db_session.query(CheckingManagement).filter(CheckingManagement.AccNum == accnum)
        if manage.first() is None:
            raise NotFind('Account management not find')
        acc.update(newinfo)
        alterBankAsset(manage.first().SubName, float(newinfo['Balance'])-acc.first().Balance)
        db_session.commit()
    elif acctype == 'Saving':
        if len(newinfo) < len(Saving.__table__.columns):
            raise IncompleteData
        acc = db_session.query(Saving).filter(Saving.AccNum == accnum)
        if acc.first() is None:
            raise NotFind('Account not find')
        manage = db_session.query(SavingManagement).filter(SavingManagement.AccNum == accnum)
        if manage.first() is None:
            raise NotFind('Account management not find')
        alterBankAsset(manage.first().SubName, float(newinfo['Balance'])-acc.first().Balance)
        acc.update(newinfo)
        db_session.commit()
    else:
        raise UndefindBehaviour

'''
return explicit accountinfo from Account table
input: acctype(str), accnum(str)
acctype == 'Checking' or 'Saving'
'''
def getAccountInfo(acctype, accnum):
    if acctype == 'Checking':
        t = db_session.query(Checking).filter(Checking.AccNum == accnum)
    elif acctype == 'Saving':
        t = db_session.query(Saving).filter(Saving.AccNum == accnum)
    else:
        raise UndefindBehaviour
    if t is None:
        raise NotFind
    return t

'''
return all accountinfo from Account table
input: acctype(str)
acctype == 'Checking' or 'Saving'
'''
def getAllAccountInfo(acctype):
    if acctype == 'Checking':
        t = db_session.query(Checking).all()
    elif acctype == 'Saving':
        t = db_session.query(Saving).all()
    else:
        raise UndefindBehaviour
    return t

'''
return all account in subname bank from Management table
input: acctype(str), subname(str)
acctype == 'Checking' or 'Saving'
'''
def getAllAccountBySubName(acctype, subname):
    if acctype == 'Checking':
        t = db_session.query(CheckingManagement).filter(CheckingManagement.SubName == subname).all()
    elif acctype == 'Saving':
        t = db_session.query(SavingManagement).filter(SavingManagement.SubName == subname).all()
    else:
        raise UndefindBehaviour
    if t is None:
        raise NotFind
    return t

'''
return all account owned by id from Management table
input: acctype(str), id(str)
acctype == 'Checking' or 'Saving'
'''
def getAllAccountByID(acctype, id):
    if acctype == 'Checking':
        t = db_session.query(CheckingManagement).filter(CheckingManagement.ID == id).all()
    elif acctype == 'Saving':
        t = db_session.query(SavingManagement).filter(SavingManagement.ID == id).all()
    else:
        raise UndefindBehaviour
    if t is None:
        raise NotFind
    return t

'''
return account number owned by id and in subname bank from Management table
input: acctype(str), id(str), subname(str)
acctype == 'Checking' or 'Saving'
'''
def getAccountBySubAndID(acctype, id, subname):
    if acctype == 'Checking':
        t = db_session.query(CheckingManagement).filter(CheckingManagement.ID == id, CheckingManagement.SubName == subname)
    elif acctype == 'Saving':
        t = db_session.query(SavingManagement).filter(SavingManagement.ID == id, SavingManagement.SubName == subname)
    else:
        raise UndefindBehaviour
    if t is None:
        raise NotFind
    return t

'''
create new loan
input: info(dict), userlist(list)
info include SubName, LoanNum, Budget
userlist is the list of user ID
'''
def createLoan(info, userlist):
    if len(info) < len(Loan.__table__.columns):
        raise IncompleteData
    if db_session.query(Loan).filter(Loan.LoanNum == info['LoanNum']).first() is not None:
        raise DupId('Duplicated Loan')
    if db_session.query(Subbranch).filter(Subbranch.SubName == info['SubName']).first() is None:
        raise NotFind('Not Find Subbranch')
    users = []
    for user in userlist:
        p = db_session.query(User).filter(User.ID == user).first()
        if p is None:
            raise NotFind('Not Find User')
        users.append(p)
    l = Loan(info)
    for p in users:
        p.Loan.append(l)
        db_session.add(p)
    db_session.commit()

# '''
# add Loan user relationship
# input: info(dict)
# info include SubName, LoanNum, ID
# '''
# def addUser2Loan(info):
#     l = db_session.query(Loan).filter(Loan.LoanNum == info['LoanNum']).first()
#     if l is None:
#         raise NotFind('Loan')
#     p = db_session.query(User).filter(User.ID == info['ID']).first()
#     if p is None:
#         raise NotFind('Not Find User')
#     if db_session.query(Subbranch).filter(Subbranch.SubName == info['SubName']).first() is None:
#         raise NotFind('Not Find Subbranch')
#     del info['ID']
#     if len(info) < len(Loan.__table__.columns):
#         raise IncompleteData
#     # if l in p.Loan:
#     #     raise DupId
#     return p
#     # p.loan.append(l)
#     # db_session.add(p)
#     # db_session.commit()

'''
get all loan
'''
def getAllLoan():
    return db_session.query(Loan).all()

'''
return explicit Loan from Loan table
input: loannum(str)
'''
def getLoanByLoanNum(loannum):
    t = db_session.query(Loan).filter(Loan.LoanNum == loannum).first()
    if t is None:
        raise NotFind
    return t

'''
return all Loan owned by id from Possess table
input: id(str)
'''
def getAllLoanByID(id):
    t = db_session.query(User).filter(User.ID == id).first()
    if t is None:
        raise NotFind
    return t.Loan

'''
get paied money for explicit loan
input: loannum(str)
return: paied amount(Float(8))
'''
def getPaiedForLoan(loannum):
    if db_session.query(Loan).filter(Loan.LoanNum == loannum).first() is None:
        raise NotFind
    g = db_session.query(PayRecord).filter(PayRecord.LoanNum == loannum).all()
    total = 0
    for grant in g:
        total += grant.Amount
    return total

'''
get loan status
input: loannum(str)
return: status(str)
status: DONE(has been granted), ING(not yet done), IDEA(not yet start)
'''
def getLoanStatus(loannum):
    paied = getPaiedForLoan(loannum)
    l = db_session.query(Loan).filter(Loan.LoanNum == loannum).first()
    if l.Budget < paied:
        raise OutOfBound
    elif paied == 0:
        return 'IDEA'
    elif l.Budget > paied:
        return 'ING'
    else:
        raise UndefindBehaviour

'''
grant loan by subbranch
input: info(dict)
info include PayNum, SubName, LoanNum, PayDate, LoanNumPay
'''
def grantLoan(info):
    if len(info) < len(PayRecord.__table__.columns):
        raise IncompleteData
    if db_session.query(PayRecord).filter(PayRecord.PayNum == info['PayNum']).first() is not None:
        raise DupId
    if db_session.query(Loan).filter(Loan.LoanNum == info['LoanNum']).first() is None:
        raise NotFind('No such Loan')
    if db_session.query(Subbranch).filter(Subbranch.SubName == info['SubName']).first() is None:
        raise NotFind('No such subbranch')
    db_session.add(PayRecord(info))
    db_session.commit()

'''
delete loan
input: id(str)
id is LoanNum
'''
def delLoan(id):
    l = db_session.query(Loan).filter(Loan.LoanNum == id)
    if l.first() is None:
        raise NotFind
    if getLoanStatus(id) == 'ING':
        raise PermissionDenied
    l.delete()
    db_session.commit()