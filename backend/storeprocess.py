from backend.model import *
from backend.exceptions import *
from sqlalchemy import Column, String, create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.database import db_session, conn
from sqlalchemy import exc
import hashlib

'''
import sql file to mysqldb by filepath
'''
def _importSqlfile(filepath):
    from subprocess import Popen, PIPE
    process = Popen(['mysql', '-u', 'root'],
                    stdout=PIPE, stdin=PIPE)
    cmd = 'use lab3; source ' + filepath + ';'
    output = process.communicate(cmd.encode('utf-8'))[0]

'''
return all workerinfo from Worker table
'''
def _getAllWorkerInfo():
    return db_session.query(Worker).all()
    
'''
add a new worker to Worker table
'''
def _createWorker(info):
    w = Worker(info)
    db_session.add(w)

'''
return explicit workerinfo from Worker table
input: id(str)
'''
def _getWorkerbyID(id):
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
# def _alterWorker(id, newinfo):
#     # w = Worker(newinfo)
#     id = int(id)
#     t = db_session.query(Worker).filter(Worker.WorkerID == id).update(newinfo)

'''
alter Bank Assets
modify assets of subbranch
SubBranch.SubAssets += change
input: subname(str), change(Float(8))
'''
def _alterBankAsset(subname, change):
    b = db_session.query(Subbranch).filter(Subbranch.SubName == subname).first()
    if b is None:
        raise NotFind
    b.SubAssets += change
    db_session.add(b)

'''
add a new user
input: info(dict)
info include ID, Address, ContectName, ContectTel,
ContectEmail, Relationship
'''
def _createUser(info):
    # if already have same ID user
    if db_session.query(User).filter(User.ID == info['ID']).first() is not None:
        raise DupId
    # 
    if len(info) < len(User.__table__.columns):
        raise IncompleteData
    p = User(info)
    db_session.add(p)

'''
delete userinfo by id
input: id(str)
'''
def _delUser(id):
    if db_session.query(User).filter(User.ID == id).first() is None:
        raise NotFind
    try:
        db_session.query(User).filter(User.ID == id).delete()
    except exc.IntegrityError:
        raise Unmodifiable("Can't delete item with foreign key")

'''
alter user
input: id(str), newinfo(dict)
newinfo include ID, Address, ContectName, ContectTel,
ContectEmail, Relationship
'''
def _alterUser(id, newinfo):
    if id != newinfo['ID']:
        raise Unmodifiable
    if db_session.query(User).filter(User.ID == id).first() is None:
        raise NotFind
    if len(newinfo) < len(User.__table__.columns):
        raise IncompleteData
    db_session.query(User).filter(User.ID == id).update(newinfo)

'''
return userinfo from User table
'''
def _getUserInfo(info):
    t = db_session.query(User)
    if 'ID' in info and len(info['ID']) != 0:
        t = t.filter(User.ID.like('%'+info['ID']+'%'))
    if 'Address' in info and len(info['Address']) != 0:
        t = t.filter(User.Address.like('%'+info['Address']+'%'))
    if 'ContectName' in info and len(info['ContectName']) != 0:
        t = t.filter(User.ContectName.like('%'+info['ContectName']+'%'))
    if 'ContectTel' in info and len(info['ContectTel']) != 0:
        t = t.filter(User.ContectTel.like('%'+info['ContectTel']+'%'))
    if 'ContectEmail' in info and len(info['ContectEmail']) != 0:
        t = t.filter(User.ContectEmail.like('%'+info['ContectEmail']+'%'))
    if 'Relationship' in info and len(info['Relationship']) != 0:
        t = t.filter(User.Relationship.like('%'+info['Relationship']+'%'))
    return t.all() 

'''
return all userinfo from User table
'''
def _getAllUserInfo():
    return db_session.query(User).all()

'''
return explicit userinfo from User table
input: id(str)
'''
def _getUserbyID(id):
    if id == '':
        raise UndefindBehaviour
    t = db_session.query(User).filter(User.ID.like('%'+id+'%'))
    if t is None:
        raise NotFind
    return t

'''
return explicit userinfo from User table
input: accnum(str)
'''
def _getUserbyAccount(accnum):
    if accnum == '':
        raise UndefindBehaviour
    type = _getAccountType(accnum)
    if type == 'Checking':
        a = db_session.query(CheckingManagement).filter(CheckingManagement.AccNum.like('%'+accnum+'%'))
        t = db_session.query(User).filter(User.ID == a.ID)
    else:
        a = db_session.query(SavingManagement).filter(SavingManagement.AccNum.like('%'+accnum+'%'))
        t = db_session.query(User).filter(User.ID == a.ID)
    if t is None:
        raise NotFind
    return t

'''
add relate between Worker and User
input: info(dict)
info include WorkerID, ID and Role
'''
def _addRelate(info):
    if db_session.query(User).filter(User.ID == info['ID']).first() is None:
        raise NotFind("Not find User")
    if db_session.query(Worker).filter(Worker.ID == info['WorkerID']).first() is None:
        raise NotFind("Not find Worker")
    if db_session.query(Relate).filter(Relate.ID == info['ID'], Relate.WorkerID == info['WorkerID']).first() is not None:
        raise DupId
    if len(info) < len(Relate.__table__.columns):
        raise IncompleteData
    db_session.add(Relate(info))

'''
alter relate between Worker and User
input: info(dict)
info include WorkerID, ID and Role
'''
def _alterRelate(newinfo):
    if db_session.query(Relate).filter(Relate.ID == newinfo['ID'], Relate.WorkerID == newinfo['WorkerID']).first() is None:
        raise NotFind
    if len(newinfo) < len(Relate.__table__.columns):
        raise IncompleteData
    db_session.query(Relate).filter(Relate.ID == newinfo['ID'], Relate.WorkerID == newinfo['WorkerID']).update(newinfo)

'''
add account
input: acctype(str), info(dict)
acctype == 'Checking' or 'Saving'
info include AccNum, ID, Balance, OpenDate, SubName, Rate, CurrencyType, Overdraft
'''
def _createAccount(acctype, info):
    if 'LastAccessTime' in info:
        del info['LastAccessTime']
    if db_session.query(Account).filter(Account.AccNum == info['AccNum']).first() is not None:
        raise DupId
    try:
        if acctype == 'Checking':
            # db_session.add(Checking(info))
            # db_session.add(CheckingManagement(info))
            if db_session.query(CheckingManagement).filter(CheckingManagement.ID == info['ID'], CheckingManagement.SubName == info['SubName']).first() is not None:
                raise DupId('Duplicated account in same subbranch')
            Transactions = conn.begin()
            conn.execute(
                """
                INSERT INTO Account (AccNum, Balance, OpenDate) 
                VALUES (%s, %s, %s);
                """,
                (info['AccNum'], info['Balance'], info['OpenDate'])
            )
            conn.execute(
                '''
                INSERT INTO Checking (AccNum, Overdraft) 
                VALUES (%s, %s)
                ''',
                (info['AccNum'], info['Overdraft'])
            )
            conn.execute(
                '''
                INSERT INTO CheckingManagement (ID, SubName, AccNum) 
                VALUES (%s, %s, %s)
                ''',
                (info['ID'], info['SubName'], info['AccNum'])
            )
        elif acctype == 'Saving':
            # db_session.add(Account(info))
            # db_session.add(Saving(info))
            # db_session.add(SavingManagement(info))
            if db_session.query(SavingManagement).filter(SavingManagement.ID == info['ID'], SavingManagement.SubName == info['SubName']).first() is not None:
                raise DupId('Duplicated account in same subbranch')
            Transactions = conn.begin()
            conn.execute(
                """
                INSERT INTO Account (AccNum, Balance, OpenDate) 
                VALUES (%s, %s, %s);
                """,
                (info['AccNum'], info['Balance'], info['OpenDate'])
            )
            conn.execute(
                '''
                INSERT INTO Saving (AccNum, Rate, CurrencyType) 
                VALUES (%s, %s, %s)
                ''',
                (info['AccNum'], info['Rate'], info['CurrencyType'])
            )
            conn.execute(
                '''
                INSERT INTO SavingManagement (ID, SubName, AccNum) 
                VALUES (%s, %s, %s)
                ''',
                (info['ID'], info['SubName'], info['AccNum'])
            )
        else:
            raise UndefindBehaviour
    except KeyError:
        Transactions.rollback()
        raise IncompleteData
    _alterBankAsset(info['SubName'], float(info['Balance']))
    return Transactions

'''
delete account
input: accnum(str)
'''
def _delAccount(accnum):
    acc = db_session.query(Account).filter(Account.AccNum == accnum)
    if acc.first() is None:
        raise NotFind
    type = _getAccountType(accnum)
    if type == 'Checking':
        accm = db_session.query(CheckingManagement).filter(CheckingManagement.AccNum == accnum)
        accn = db_session.query(Checking).filter(Checking.AccNum == accnum)
    else:
        accm = db_session.query(SavingManagement).filter(SavingManagement.AccNum == accnum)
        accn = db_session.query(Saving).filter(Saving.AccNum == accnum)
    _alterBankAsset(accm.first().SubName, -acc.first().Balance)
    accm.delete()
    accn.delete()
    acc.delete()

'''
alter accountinfo
input: acctype(str), accnum(str), newinfo(dict)
acctype == 'Checking' or 'Saving'
newinfo include AccNum, Balance, LastAccessTime, OpenDate
'''
def _alterAccount(acctype, accnum, newinfo):
    if accnum != newinfo['AccNum']:
        raise Unmodifiable
    accinfo = {}
    accparentinfo = {}
    for c in Account.__table__.columns:
        if c.name in newinfo:
            accparentinfo[c.name] = newinfo[c.name]
    if acctype == 'Checking':
        for c in Checking.__table__.columns:
            if c.name in newinfo:
                accinfo[c.name] = newinfo[c.name]
        if len(newinfo) < len(Checking.__table__.columns):
            raise IncompleteData
        acc = db_session.query(Checking).filter(Checking.AccNum == accnum)
        accparent = db_session.query(Account).filter(Account.AccNum == accnum)
        if acc.first() is None or accparent.first() is None:
            raise NotFind('Account not find')
        manage = db_session.query(CheckingManagement).filter(CheckingManagement.AccNum == accnum)
        if manage.first() is None:
            raise NotFind('Account management not find')
        _alterBankAsset(manage.first().SubName, float(newinfo['Balance'])-acc.first().Balance)
        acc.update(accinfo)
        accparent.update(accparentinfo)
    elif acctype == 'Saving':
        for c in Saving.__table__.columns:
            if c.name in newinfo:
                accinfo[c.name] = newinfo[c.name]
        if len(newinfo) < len(Saving.__table__.columns):
            raise IncompleteData
        acc = db_session.query(Saving).filter(Saving.AccNum == accnum)
        accparent = db_session.query(Account).filter(Account.AccNum == accnum)
        if acc.first() is None or accparent.first() is None:
            raise NotFind('Account not find')
        manage = db_session.query(SavingManagement).filter(SavingManagement.AccNum == accnum)
        if manage.first() is None:
            raise NotFind('Account management not find')
        _alterBankAsset(manage.first().SubName, float(newinfo['Balance'])-acc.first().Balance)
        acc.update(accinfo)
        accparent.update(accparentinfo)
    else:
        raise UndefindBehaviour

'''
add a user to acount
input ID(str), accnum(str)
'''
def _addUser2Account(ID, accnum):
    if db_session.query(User).filter(User.ID == ID).first() is None:
        raise NotFind('Not find user')
    acctype = _getAccountType(accnum)
    if acctype == 'Saving':
        acc = db_session.query(SavingManagement).filter(SavingManagement.AccNum == accnum).first()
        if db_session.query(CheckingManagement).filter(SavingManagement.ID == ID, SavingManagement.SubName == acc.SubName).first() is not None:
            raise DupId
        db_session.add(SavingManagement({'ID':ID, 'AccNum':accnum, 'SubName':acc.SubName}))
    elif acctype == 'Checking':
        acc = db_session.query(CheckingManagement).filter(CheckingManagement.AccNum == accnum).first() 
        if db_session.query(CheckingManagement).filter(CheckingManagement.ID == ID, CheckingManagement.SubName == acc.SubName).first() is not None:
            raise DupId
        db_session.add(CheckingManagement({'ID':ID, 'AccNum':accnum, 'SubName':acc.SubName}))

'''
get account type
input accnum(str)
return 'Checking' or 'Saving'
'''
def _getAccountType(accnum):
    if db_session.query(Checking).filter(Checking.AccNum == accnum).first() is not None:
        return 'Checking'
    elif db_session.query(Saving).filter(Saving.AccNum == accnum).first() is not None:
        return 'Saving'
    else:
        raise NotFind

'''
return explicit accountinfo from Checking or Saving table
input: acctype(str), accnum(str)
acctype == 'Checking' or 'Saving'
'''
def _getAccountInfo(acctype, accnum):
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
def _getAllAccountInfo(acctype):
    if acctype == 'Checking':
        t = db_session.query(Checking, Account).all()
    elif acctype == 'Saving':
        t = db_session.query(Saving, Account).all()
    else:
        raise UndefindBehaviour
    return t

'''
return all account in subname bank from Management table
input: acctype(str), subname(str)
acctype == 'Checking' or 'Saving'
'''
def _getAllAccountBySubName(acctype, subname):
    if acctype == 'Checking':
        t = db_session.query(Checking, CheckingManagement, Account).filter(Account.AccNum == Checking.AccNum, Checking.AccNum == CheckingManagement.AccNum, CheckingManagement.SubName == subname).all()
        # t = db_session.query(CheckingManagement).filter(CheckingManagement.SubName == subname).all()
    elif acctype == 'Saving':
        t = db_session.query(Saving, SavingManagement, Account).filter(Account.AccNum == Saving.AccNum, Saving.AccNum == SavingManagement.AccNum, SavingManagement.SubName == subname).all()
        # t = db_session.query(SavingManagement).filter(SavingManagement.SubName == subname).all()
    else:
        raise UndefindBehaviour
    return t

'''
return all account owned by id from Management table
input: acctype(str), id(str)
acctype == 'Checking' or 'Saving'
'''
def _getAccountByID(acctype, id):
    if acctype == 'Checking':
        t = db_session.query(Checking, CheckingManagement, Account).filter(Account.AccNum == Checking.AccNum, Checking.AccNum == CheckingManagement.AccNum, CheckingManagement.ID == id).all()
    elif acctype == 'Saving':
        t = db_session.query(Saving, SavingManagement, Account).filter(Account.AccNum == Saving.AccNum, Saving.AccNum == SavingManagement.AccNum, SavingManagement.ID == id).all()
    else:
        raise UndefindBehaviour
    return t

'''
return all account owned by id from Management table
input: acctype(str), id(str)
acctype == 'Checking' or 'Saving'
'''
def _getAccount(info):
    sel = 0
    if 'AccType' in info and len(info['AccType']) != 0:
        if(info['AccType'] == 'Checking'):
            sel = 1
        elif(info['AccType'] == 'Saving'):
            sel = 2
        else:
            raise UndefindBehaviour
    if sel != 2:
        t = db_session.query(Checking, CheckingManagement, Account).filter(Account.AccNum == Checking.AccNum, Checking.AccNum == CheckingManagement.AccNum)
        if 'ID' in info and len(info['ID']) != 0:
            t = t.filter(CheckingManagement.ID.like('%'+info['ID']+'%'))
        if 'AccNum' in info and len(info['AccNum']) != 0:
            t = t.filter(CheckingManagement.AccNum.like('%'+info['AccNum']+'%'))
        if 'BalanceMin' in info and len(info['BalanceMin']) != 0:
            t = t.filter(Account.Balance >= info['BalanceMin'])
        if 'BalanceMax' in info and len(info['BalanceMax']) != 0:
            t = t.filter(Account.Balance <= info['BalanceMax'])
        if 'SubName' in info and len(info['SubName']) != 0:
            t = t.filter(CheckingManagement.SubName.like('%'+info['SubName']+'%'))
        # if 'ContectTel' in info and len(info['ContectTel']) != 0:
        #     t = t.filter(User.ContectTel.like('%'+info['ContectTel']+'%'))
        # if 'ContectEmail' in info and len(info['ContectEmail']) != 0:
        #     t = t.filter(User.ContectEmail.like('%'+info['ContectEmail']+'%'))
        # if 'Relationship' in info and len(info['Relationship']) != 0:
        #     t = t.filter(User.Relationship.like('%'+info['Relationship']+'%'))
    if sel != 1:
        s = db_session.query(Saving, SavingManagement, Account).filter(Account.AccNum == Saving.AccNum, Saving.AccNum == SavingManagement.AccNum)
        if 'ID' in info and len(info['ID']) != 0:
            s = s.filter(SavingManagement.ID.like('%'+info['ID']+'%'))
        if 'AccNum' in info and len(info['AccNum']) != 0:
            s = s.filter(SavingManagement.AccNum.like('%'+info['AccNum']+'%'))
        if 'BalanceMin' in info and len(info['BalanceMin']) != 0:
            s = s.filter(Account.Balance >= info['BalanceMin'])
        if 'BalanceMax' in info and len(info['BalanceMax']) != 0:
            s = s.filter(Account.Balance <= info['BalanceMax'])
        if 'SubName' in info and len(info['SubName']) != 0:
            s = s.filter(SavingManagement.SubName.like('%'+info['SubName']+'%'))
        # if 'ContectTel' in info and len(info['ContectTel']) != 0:
        #     s = s.filter(User.ContectTel.like('%'+info['ContectTel']+'%'))
        # if 'ContectEmail' in info and len(info['ContectEmail']) != 0:
        #     s = s.filter(User.ContectEmail.like('%'+info['ContectEmail']+'%'))
        # if 'Relationship' in info and len(info['Relationship']) != 0:
        #     s = s.filter(User.Relationship.like('%'+info['Relationship']+'%'))
    if sel == 1:
        return t.all()
    if sel == 2:
        return s.all()
    else:
        # return t.group_by(Account.AccNum).all()+s.group_by(Account.AccNum).all()
        return t.all()+s.all()

'''
return account number owned by id and in subname bank from Management table
input: acctype(str), id(str), subname(str)
acctype == 'Checking' or 'Saving'
'''
def _getAccountBySubAndID(acctype, id, subname):
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
def _createLoan(info, userlist):
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

# '''
# add Loan user relationship
# input: info(dict)
# info include SubName, LoanNum, ID
# '''
# def _addUser2Loan(info):
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

'''
get all loan
'''
def _getAllLoan():
    return db_session.query(Loan).all()

'''
return explicit Loan from Loan table
input: loannum(str)
'''
def _getLoanByLoanNum(loannum):
    t = db_session.query(Loan).filter(Loan.LoanNum == loannum).first()
    return t

'''
return all Loan owned by id from Possess table
input: id(str)
'''
def _getAllLoanByID(id):
    t = db_session.query(User).filter(User.ID == id).first()
    return t.Loan

'''
get paied money for explicit loan
input: loannum(str)
return: paied amount(Float(8))
'''
def _getPaiedForLoan(loannum):
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
status: DONE(has been granted), ING(not yet done), IDLE(not yet start)
'''
def _getLoanStatus(loannum):
    paied = _getPaiedForLoan(loannum)
    l = db_session.query(Loan).filter(Loan.LoanNum == loannum).first()
    if l.Budget < paied:
        raise OutOfBound
    elif paied == 0:
        return 'IDLE'
    elif l.Budget > paied:
        return 'ING'
    elif l.Budget == paied:
        return 'DONE'
    else:
        raise UndefindBehaviour

'''
grant loan by subbranch
input: info(dict)
info include PayNum, SubName, LoanNum, PayDate, Amount
'''
def _grantLoan(info):
    if len(info) < len(PayRecord.__table__.columns):
        raise IncompleteData
    if db_session.query(PayRecord).filter(PayRecord.PayNum == info['PayNum']).first() is not None:
        raise DupId
    if db_session.query(Loan).filter(Loan.LoanNum == info['LoanNum']).first() is None:
        raise NotFind('No such Loan')
    if db_session.query(Subbranch).filter(Subbranch.SubName == info['SubName']).first() is None:
        raise NotFind('No such subbranch')
    if _getPaiedForLoan(info['LoanNum']) + float(info['Amount']) > _getLoanByLoanNum(info['LoanNum']).Budget:
        raise OutOfBound
    db_session.add(PayRecord(info))
    _alterBankAsset(info['SubName'], -float(info['Amount']))

'''
delete loan
input: id(str)
id is LoanNum
'''
def _delLoan(id):
    l = db_session.query(Loan).filter(Loan.LoanNum == id)
    pay = db_session.query(PayRecord).filter(PayRecord.LoanNum == id)
    if l.first() is None:
        raise NotFind
    if _getLoanStatus(id) == 'ING':
        raise PermissionDenied
    _alterBankAsset(l.first().SubName, l.first().Budget)
    pay.delete()
    l.delete()

'''
get saving account by a special subbranch and time
input: subname(str)
return Account object list
'''
def _getSavingAccountBySubName(subname, **kw):
    if db_session.query(Subbranch).filter(Subbranch.SubName == subname).first() is None:
        raise NotFind
    if "time" in kw and len(kw['time']) == 2 and len(kw['time']['start']) and len(kw['time']['end']):
        return db_session.query(Saving, Account).filter(Saving.AccNum == Account.AccNum).join(SavingManagement).filter(SavingManagement.SubName == subname, Account.OpenDate >= kw['time']['start'], Account.OpenDate <= kw['time']['end']).all()
    else:
        return db_session.query(Saving).join(SavingManagement).filter(SavingManagement.SubName == subname).all()

'''
get saving total by a special subbranch
input: subname(str)
return float
'''
def _getSavingNumBySubName(subname, **kw):
    if "time" in kw:
        saving = _getSavingAccountBySubName(subname, time=kw['time'])
        return sum([account[0].Balance for account in saving])
    else:
        saving = _getSavingAccountBySubName(subname)
        return sum([account.Balance for account in saving])

'''
get checking account by a special subbranch and time
input: subname(str)
return Account object list
'''
def _getCheckingAccountBySubName(subname, **kw):
    if db_session.query(Subbranch).filter(Subbranch.SubName == subname).first() is None:
        raise NotFind
    if "time" in kw and len(kw['time']) == 2 and len(kw['time']['start']) and len(kw['time']['end']):
        return db_session.query(Checking, Account).filter(Checking.AccNum == Account.AccNum).join(CheckingManagement).filter(CheckingManagement.SubName == subname, Account.OpenDate >= kw['time']['start'], Account.OpenDate <= kw['time']['end']).all()
    else:
        return db_session.query(Checking).join(CheckingManagement).filter(CheckingManagement.SubName == subname).all()

'''
get checking total by a special subbranch and time
input: subname(str), kw(time={"start":"2020-10-5", "end":"2021-10-5"})
return float
'''
def _getCheckingNumBySubName(subname, **kw):
    if "time" in kw:
        checking = _getCheckingAccountBySubName(subname, time=kw['time'])
        return sum([account[0].Balance for account in checking])
    else:
        checking = _getCheckingAccountBySubName(subname)
        return sum([account.Balance for account in checking])

'''
get loan paied total by a special subbranch and time
input: subname(str), kw(time={"start":"2020-10-5", "end":"2021-10-5"})
return float
'''
def _getLoanPaiedBySubName(subname, **kw):
    if "time" in kw and len(kw['time']) == 2 and len(kw['time']['start']) and len(kw['time']['end']):
        payrecord = db_session.query(PayRecord).filter(PayRecord.SubName == subname, PayRecord.PayDate >= kw['time']['start'], PayRecord.PayDate <= kw['time']['end']).all()
    else:
        payrecord = db_session.query(PayRecord).filter(PayRecord.SubName == subname).all()
    return sum([pay.Amount for pay in payrecord])

'''
return subbranch data from Subbranch table
'''
def _getAllSubInfo():
    return db_session.query(Subbranch).all()

'''
return subbranch data from Subbranch table by subbranch name
'''
def _getSubInfoByName(subname):
    return db_session.query(Subbranch).filter(Subbranch.SubName == subname).all()

'''
auth admin
'''
def _auth(username, password):
    a = db_session.query(Admin).filter(Admin.username == username).first()
    if a is None:
        raise NotFind
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return a.password == sha256.hexdigest()
    
'''
add admin
'''
def _addAdmin(username, password):
    a = db_session.query(Admin).filter(Admin.username == username).first()
    if a is not None:
        raise DupId
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    db_session.add(Admin({
        "username": username,
        "password": sha256.hexdigest()
    }))

'''
get admin
'''
def _getAdmin(username):
    return db_session.query(Admin).filter(Admin.username == username).first()
    