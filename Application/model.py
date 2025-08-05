from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Insert, Delete, Integer, String, Update,and_
from flask import current_app as app

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    uid = db.Column(Integer, primary_key=True)
    uname = db.Column(String)
    passwd = db.Column(Integer)

    def insertUser(uname,hashed):
        query = Insert(User).values(uname=uname,passwd=hashed)
        db.session.execute(query)
        db.session.commit()

class Contests(db.Model):
    __tablename__ = "Contests"
    cid = db.Column(Integer, primary_key=True)
    cname = db.Column(String, unique=True)

    def get_all():
        return Contests.query.all()

class Problems(db.Model):
    __tablename__ = "Problems"
    pid = db.Column(Integer, primary_key=True, autoincrement=True)
    pname = db.Column(String)
    pdesc = db.Column(String)
    ahash = db.Column(String)

class contestProblems(db.Model):
    __tablename__ = "contestProblems"
    eid = db.Column(Integer, primary_key=True)
    cid = db.Column(Integer, db.ForeignKey('Contests.cid'))
    pid = db.Column(Integer, db.ForeignKey('Problems.pid'))


class Submissions(db.Model):
    __tablename__ = "Submissions"
    sid = db.Column(Integer, primary_key=True,autoincrement=True)
    cid = db.Column(Integer,  db.ForeignKey('Contests.cid') , index = True)
    uid = db.Column(Integer, db.ForeignKey('User.uid') , index = True)
    pid = db.Column(Integer, db.ForeignKey('Problems.pid'))
    shash = db.Column(String)
    stime = db.Column(String)
    ispass = db.Column(Integer)

class Enrolled(db.Model):
    __tablename__ = "Enrolled"
    eid = db.Column(Integer, primary_key=True)
    cid = db.Column(Integer,  db.ForeignKey('Contests.cid') , index = True)
    uid = db.Column(Integer, db.ForeignKey('User.uid'))

    def isenrolled(uid,cid):
        for i in Enrolled.query.all():
            if i.cid == cid and i.uid == uid:
                return True
        return False

    def enroll(uid,cid):
        query = Insert(Enrolled).values(uid = uid,cid = cid)
        try:
            db.session.execute(query)
            db.session.commit()
            return True
        except:
            return False


