/*==============================================================*/
/* DBMS name:
/* Created on:
/*==============================================================*/
SET FOREIGN_KEY_CHECKS = 0;
drop table if exists Account;
drop table if exists Checking;
drop table if exists CheckingManagement;
drop table if exists Department;
drop table if exists Loan;
drop table if exists Manager;
drop table if exists PayRecord;
drop table if exists Saving;
drop table if exists SavingManagement;
drop table if exists Subbranch;
drop table if exists User;
drop table if exists Worker;
drop table if exists possess;
drop table if exists Relate;
SET FOREIGN_KEY_CHECKS = 1;
drop table if exists possess;

/*==============================================================*/
/* Table: Account                                               */
/*==============================================================*/
create table Account
(
   AccNum               numeric(19,0) not null  comment '',
   Balance              float(8,2) not null  comment '',
   LastAccessTime       datetime  comment '',
   OpenDate             date not null  comment '',
   primary key (AccNum)
);

/*==============================================================*/
/* Table: Checking                                              */
/*==============================================================*/
create table Checking
(
   AccNum               numeric(19,0) not null  comment '',
   Overdraft            float(8,2) not null  comment '',
   primary key (AccNum)
);

/*==============================================================*/
/* Table: CheckingManagement                                    */
/*==============================================================*/
create table CheckingManagement
(
   ID                   char(18) not null  comment '',
   SubName              varchar(50) not null  comment '',
   AccNum               numeric(19,0) not null  comment '',
   primary key (ID, SubName)
);

/*==============================================================*/
/* Table: Department                                            */
/*==============================================================*/
create table Department
(
   SubName              varchar(50) not null  comment '',
   DepartNum            numeric(8,0) not null  comment '',
   DepartName           varchar(50)  comment '',
   DepartType           int  comment '',
   primary key (SubName, DepartNum)
);

/*==============================================================*/
/* Table: Loan                                                  */
/*==============================================================*/
create table Loan
(
   SubName              varchar(50) not null  comment '',
   Budget               float(8,2) not null  comment '',
   LoanNum              numeric(8,0) not null  comment '',
   primary key (SubName, LoanNum)
);

/*==============================================================*/
/* Table: Manager                                               */
/*==============================================================*/
create table Manager
(
   WorkerID             char(18) not null  comment '',
   SubName              varchar(50) not null  comment '',
   DepartNum            numeric(8,0) not null  comment '',
   primary key (WorkerID)
);

/*==============================================================*/
/* Table: PayRecord                                             */
/*==============================================================*/
create table PayRecord
(
   PayNum               int not null  comment '',
   SubName              varchar(20)  comment '',
   LoanNum              numeric(8,0)  comment '',
   PayDate              date  comment '',
   Amount               float(8,2)  comment '',
   primary key (PayNum)
);

/*==============================================================*/
/* Table: Relate                                                */
/*==============================================================*/
create table Relate
(
   WorkerID             char(18) not null  comment '',
   ID                   char(18) not null  comment '',
   Role                 bool  comment '',
   primary key (WorkerID, ID)
);

/*==============================================================*/
/* Table: Saving                                                */
/*==============================================================*/
create table Saving
(
   AccNum               numeric(19,0) not null  comment '',
   Rate                 float not null  comment '',
   CurrencyType         int not null  comment '',
   primary key (AccNum)
);

/*==============================================================*/
/* Table: SavingManagement                                      */
/*==============================================================*/
create table SavingManagement
(
   ID                   char(18) not null  comment '',
   SubName              varchar(50) not null  comment '',
   AccNum               numeric(19,0) not null  comment '',
   primary key (ID, SubName)
);

/*==============================================================*/
/* Table: Subbranch                                             */
/*==============================================================*/
create table Subbranch
(
   SubName              varchar(50) not null  comment '',
   SubAssets            float(8,2)  comment '',
   City                 varchar(50)  comment '',
   primary key (SubName)
);

/*==============================================================*/
/* Table: User                                                  */
/*==============================================================*/
create table User
(
   ID                   char(18) not null  comment '',
   Address              text  comment '',
   ContectName          varchar(20) not null  comment '',
   ContectTel           numeric(11,0) not null  comment '',
   ContectEmail         varchar(50) not null  comment '',
   Relationship         varchar(20) not null  comment '',
   primary key (ID)
);

/*==============================================================*/
/* Table: Worker                                                */
/*==============================================================*/
create table Worker
(
   SubName              varchar(50) not null  comment '',
   DepartNum            numeric(8,0) not null  comment '',
   WorkerID             char(18) not null  comment '',
   WorkerAddr           text  comment '',
   StartDate            date  comment '',
   primary key (WorkerID)
);

/*==============================================================*/
/* Table: possess                                               */
/*==============================================================*/
create table possess
(
   SubName              varchar(20) not null  comment '',
   LoanNum              numeric(8,0) not null  comment '',
   ID                   char(18) not null  comment '',
   primary key (LoanNum, ID)
);

alter table Checking add constraint FK_CHECKING_INHERITAN_ACCOUNT foreign key (AccNum)
      references Account (AccNum) on delete restrict on update restrict;

alter table CheckingManagement add constraint FK_CHECKING_MANAGECHE_CHECKING foreign key (AccNum)
      references Checking (AccNum) on delete restrict on update restrict;

alter table CheckingManagement add constraint FK_CHECKING_RELATIONS_SUBBRANC foreign key (SubName)
      references Subbranch (SubName) on delete restrict on update restrict;

alter table CheckingManagement add constraint FK_CHECKING_RELATIONS_USER foreign key (ID)
      references User (ID) on delete restrict on update restrict;

alter table Department add constraint FK_DEPARTME_RELATIONS_SUBBRANC foreign key (SubName)
      references Subbranch (SubName) on delete restrict on update restrict;

alter table Loan add constraint FK_LOAN_HAVE_SUBBRANC foreign key (SubName)
      references Subbranch (SubName) on delete restrict on update restrict;

alter table Manager add constraint FK_MANAGER_INHERITAN_WORKER foreign key (WorkerID)
      references Worker (WorkerID) on delete restrict on update restrict;

alter table Manager add constraint FK_MANAGER_MANAGE_DEPARTME foreign key (SubName, DepartNum)
      references Department (SubName, DepartNum) on delete restrict on update restrict;

alter table PayRecord add constraint FK_PAYRECOR_PAY_LOAN foreign key (SubName, LoanNum)
      references Loan (SubName, LoanNum) on delete restrict on update restrict;

alter table Relate add constraint FK_RELATE_RELATE_WORKER foreign key (WorkerID)
      references Worker (WorkerID) on delete restrict on update restrict;

alter table Relate add constraint FK_RELATE_RELATE2_USER foreign key (ID)
      references User (ID) on delete restrict on update restrict;

alter table Saving add constraint FK_SAVING_INHERITAN_ACCOUNT foreign key (AccNum)
      references Account (AccNum) on delete restrict on update restrict;

alter table SavingManagement add constraint FK_SAVINGMA_MANAGESAV_SAVING foreign key (AccNum)
      references Saving (AccNum) on delete restrict on update restrict;

alter table SavingManagement add constraint FK_SAVINGMA_RELATIONS_USER foreign key (ID)
      references User (ID) on delete restrict on update restrict;

alter table SavingManagement add constraint FK_SAVINGMA_RELATIONS_SUBBRANC foreign key (SubName)
      references Subbranch (SubName) on delete restrict on update restrict;

alter table Worker add constraint FK_WORKER_RELATIONS_DEPARTME foreign key (SubName, DepartNum)
      references Department (SubName, DepartNum) on delete restrict on update restrict;

alter table possess add constraint FK_POSSESS_POSSESS_LOAN foreign key (SubName, LoanNum)
      references Loan (SubName, LoanNum) on delete restrict on update restrict;

alter table possess add constraint FK_POSSESS_POSSESS2_USER foreign key (ID)
      references User (ID) on delete restrict on update restrict;

