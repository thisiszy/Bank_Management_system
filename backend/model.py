# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}
Base.to_dict = to_dict

def __init__(self, data):
    for c in self.__table__.columns:
        if c.name in data:
            setattr(self, c.name, data[c.name])
Base.__init__ = __init__


class Admin(Base):
    __tablename__ = 'Admin'

    username = Column(CHAR(19), primary_key=True)
    password = Column(CHAR(100), nullable=False)

class Account(Base):
    __tablename__ = 'Account'

    AccNum = Column(DECIMAL(19, 0), primary_key=True)
    Balance = Column(Float(8), nullable=False)
    LastAccessTime = Column(DateTime)
    OpenDate = Column(Date, nullable=False)


class Checking(Account):
    __tablename__ = 'Checking'

    AccNum = Column(ForeignKey('Account.AccNum', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    Overdraft = Column(Float(8), nullable=False)


class Saving(Account):
    __tablename__ = 'Saving'

    AccNum = Column(ForeignKey('Account.AccNum', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    Rate = Column(Float, nullable=False)
    CurrencyType = Column(Integer, nullable=False)


class Subbranch(Base):
    __tablename__ = 'Subbranch'

    SubName = Column(String(50), primary_key=True)
    SubAssets = Column(Float(8))
    City = Column(String(50))


class User(Base):
    __tablename__ = 'User'

    ID = Column(CHAR(18), primary_key=True)
    Address = Column(Text)
    ContectName = Column(String(20), nullable=False)
    ContectTel = Column(DECIMAL(11, 0), nullable=False)
    ContectEmail = Column(String(50), nullable=False)
    Relationship = Column(String(20), nullable=False)

    Loan = relationship('Loan', secondary='possess')


class Department(Base):
    __tablename__ = 'Department'

    SubName = Column(ForeignKey('Subbranch.SubName', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    DepartNum = Column(DECIMAL(8, 0), primary_key=True, nullable=False)
    DepartName = Column(String(50))
    DepartType = Column(Integer)

    Subbranch = relationship('Subbranch')
    Worker = relationship('Worker', secondary='Manager')


class Loan(Base):
    __tablename__ = 'Loan'

    SubName = Column(ForeignKey('Subbranch.SubName', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    Budget = Column(Float(8), nullable=False)
    LoanNum = Column(DECIMAL(8, 0), primary_key=True, nullable=False)

    User = relationship('User', secondary='possess')
    Subbranch = relationship('Subbranch')


class CheckingManagement(Base):
    __tablename__ = 'CheckingManagement'

    ID = Column(ForeignKey('User.ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    SubName = Column(ForeignKey('Subbranch.SubName', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False, index=True)
    AccNum = Column(ForeignKey('Checking.AccNum', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    Checking = relationship('Checking')
    User = relationship('User')
    Subbranch = relationship('Subbranch')


class PayRecord(Base):
    __tablename__ = 'PayRecord'
    __table_args__ = (
        ForeignKeyConstraint(['SubName', 'LoanNum'], ['Loan.SubName', 'Loan.LoanNum'], ondelete='RESTRICT', onupdate='RESTRICT'),
        Index('FK_PAYRECOR_PAY_LOAN', 'SubName', 'LoanNum')
    )

    PayNum = Column(Integer, primary_key=True)
    SubName = Column(String(20))
    LoanNum = Column(DECIMAL(8, 0))
    PayDate = Column(Date)
    Amount = Column(Float(8))

    Loan = relationship('Loan')


class SavingManagement(Base):
    __tablename__ = 'SavingManagement'

    ID = Column(ForeignKey('User.ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    SubName = Column(ForeignKey('Subbranch.SubName', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False, index=True)
    AccNum = Column(ForeignKey('Saving.AccNum', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    Saving = relationship('Saving')
    User = relationship('User')
    Subbranch = relationship('Subbranch')


class Worker(Base):
    __tablename__ = 'Worker'
    __table_args__ = (
        ForeignKeyConstraint(['SubName', 'DepartNum'], ['Department.SubName', 'Department.DepartNum'], ondelete='RESTRICT', onupdate='RESTRICT'),
        Index('FK_WORKER_RELATIONS_DEPARTME', 'SubName', 'DepartNum')
    )

    SubName = Column(String(50), nullable=False)
    DepartNum = Column(DECIMAL(8, 0), nullable=False)
    WorkerID = Column(CHAR(18), primary_key=True)
    WorkerAddr = Column(Text)
    StartDate = Column(Date)

    Department = relationship('Department')


t_possess = Table(
    'possess', metadata,
    Column('SubName', String(20), nullable=False),
    Column('LoanNum', DECIMAL(8, 0), primary_key=True, nullable=False),
    Column('ID', ForeignKey('User.ID', ondelete='CASCADE', onupdate='RESTRICT'), primary_key=True, nullable=False, index=True),
    ForeignKeyConstraint(['SubName', 'LoanNum'], ['Loan.SubName', 'Loan.LoanNum'], ondelete='CASCADE', onupdate='RESTRICT'),
    Index('FK_POSSESS_POSSESS_LOAN', 'SubName', 'LoanNum')
)


t_Manager = Table(
    'Manager', metadata,
    Column('WorkerID', ForeignKey('Worker.WorkerID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True),
    Column('SubName', String(50), nullable=False),
    Column('DepartNum', DECIMAL(8, 0), nullable=False),
    ForeignKeyConstraint(['SubName', 'DepartNum'], ['Department.SubName', 'Department.DepartNum'], ondelete='RESTRICT', onupdate='RESTRICT'),
    Index('FK_MANAGER_MANAGE_DEPARTME', 'SubName', 'DepartNum')
)


class Relate(Base):
    __tablename__ = 'Relate'

    WorkerID = Column(ForeignKey('Worker.WorkerID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    ID = Column(ForeignKey('User.ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False, index=True)
    Role = Column(TINYINT(1))

    User = relationship('User')
    Worker = relationship('Worker')
