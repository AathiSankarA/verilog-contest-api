from Application.model import *
from Application.worker import run_verilog,create_verilog
from flask import session
from dotenv import dotenv_values
import bcrypt, hashlib, os, datetime

env = dotenv_values()
bcrypt_salt = bytes(env.get("BCRYPT_SALT","SALT"),encoding="UTF-8")

class CAuth:
    def create_user(uname , passwd):
        user = User.query.where(User.uname == uname).all()
        if user:
            return False
        hashed = bcrypt.hashpw(bytes(passwd,encoding="UTF-8"),salt=bcrypt_salt)
        User.insertUser(uname,hashed)
        return True
    
    def validate_password(uname , passwd):
        user = User.query.where(User.uname == uname).all()
        if not user:
            return False
        if user and bcrypt.checkpw(bytes(passwd,encoding="UTF-8"),user[0].passwd):
            return True,user[0].uid
        return False

class CContest:
    def list_all():
        print("hello")
        contests = Contests.query.all()
        print("hello",contests)
        li = []
        for i in contests:
            print(i.cid,session.get("user",None))
            li.append({
                    "cid" : i.cid,
                    "cname" : i.cname,
                    "enrolled" : Enrolled.isenrolled(i.cid,session.get("uid",None))
                }
            )
        return li 
    
    def contest_enroll(uid,cid):
        enrolled = Enrolled.query.where(and_(Enrolled.cid == cid ,Enrolled.uid == uid)).all()
        if enrolled:
            return True
        return Enrolled.enroll(uid,cid)
    
    def create_contest(cname):
        query = Insert(Contests).values(cname = cname)
        try:
            assert session["user"] == "Admin"
            db.session.execute(query)
            db.session.commit()
            return True
        except:
            return False
        
class CSubmission:
    def submit_code(uid,cid,pid,code):
        # try:
            time = str(datetime.datetime.strftime(datetime.datetime.now(),"%Y/%m/%d, %H:%M:%S"))
            res = str(run_verilog(code,os.path.abspath(env.get("APP_DATA")+str(pid)+".v")))
            rhash = hashlib.md5(bytes(res,encoding="UTF-8")).hexdigest()
            shash=hashlib.sha1(bytes(time+str(uid),encoding="UTF-8")).hexdigest()
            c = int(Problems.query.where(Problems.pid == pid).first().ahash == rhash)
            obj = Submissions(cid=cid,pid=pid,uid=uid,stime=time,shash=shash,ispass=c)
            db.session.add(obj)
            db.session.commit()
            file = open(env.get("APP_DATA")+str(shash)+".v","w")
            file.write(code)
            file.close()

            return {
                "message" : "submission success",
                "passed" : bool(c)
            }
        # except:
            return False
    
    def get_submissions(uid):
        res = Submissions.query.where(Submissions.uid==uid).all()
        li = []
        for i in res:
            li.append({
                "cid":i.cid,
                "pid":i.pid,
                "stime":i.stime,
                "shash":i.shash,
                "ispass":i.ispass
            })
        return li
    
    def get_all_submissions():
        res = Submissions.query.all()
        li = []
        for i in res:
            li.append({
                "cid":i.cid,
                "pid":i.pid,
                "stime":i.stime,
                "shash":i.shash,
                "ispass":i.ispass
            })
        return li
        
class CProblems:
    def delete_problem(pid):
        try:
            query = Delete(Problems).where(Problems.pid == pid)
            db.session.execute(query)
            os.remove(env.get("APP_DATA")+str(pid)+".v")
            db.session.commit()
            return True
        except:
            return False

    def edit_problem(pid,**data):
        try:
            query = Update(Problems).where(Problems.pid == pid).values(**data)
            db.session.execute(query)
            db.session.commit()
            return True
        except:
            return False
    
    def create_problem(pname,pdesc,code,tb):
        # try:
            res = create_verilog(code,tb)
            if not res:
                return "invalid"
            else:
                ans_hash = hashlib.md5(bytes(res,encoding="UTF-8")).hexdigest()
                query = Problems(pname=pname,pdesc=pdesc,ahash=ans_hash)
                db.session.add(query)
                db.session.commit()
                file = open(env.get("APP_DATA")+str(query.pid)+".v","w")
                file.write(tb)
                file.close()
                return "created"
        # except:
            return False

    def add_problem(cid,pid):
        try:
            query = Insert(contestProblems).values(cid=cid,pid =pid)
            db.session.execute(query)
            db.session.commit()
            return True
        except:
            return False

    def remove_problem(cid,pid):
        try:
            query = Delete(contestProblems).where(and_(contestProblems.cid==cid,contestProblems.pid == pid))
            db.session.execute(query)
            db.session.commit()
            return True
        except:
            return False
    def view_problems():
        try:
            li=[]
            for i in Problems.query.all():
                li.append({
                    "pid" : i.pid,
                    "pdesc" : i.pdesc,
                    "pname" : i.pname,
                })
            return li
        except:
            return False