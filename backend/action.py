import backend.storeprocess

def importSqlfile(filepath):
    backend.storeprocess._importSqlfile(filepath)


def createUser(info):
    backend.storeprocess._createUser(info)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()

def createAccount(acctype, info):
    backend.storeprocess._createAccount(acctype, info)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()

def delAccount(accnum):
    backend.storeprocess._delAccount(accnum)
    try:
        backend.storeprocess.db_session.commit()
    except Exception:
        backend.storeprocess.db_session.rollback()
