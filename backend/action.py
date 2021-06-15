import backend.storeprocess

def importSqlfile(filepath):
    backend.storeprocess._importSqlfile(filepath)


def createUser(info):
    backend.storeprocess._createUser(info)
    # try:
    backend.storeprocess.db_session.commit()
    # except:

def createAccount(acctype, info):
    backend.storeprocess._createAccount(acctype, info)
    # try:
    backend.storeprocess.db_session.commit()
    # except:

def delAccount(accnum):
    backend.storeprocess._delAccount(accnum)
    backend.storeprocess.db_session.commit()
