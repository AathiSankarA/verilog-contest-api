from flask import Blueprint, session, request
from Application.controller import CSubmission

Submission = Blueprint("submission","submission")

@Submission.post("/submit")
def submit_problem():
    uid = session.get("uid")
    if not uid:
        return {
            "message" : "login required"
        }
    data = [uid,request.json.get("cid"),request.json.get("pid"),request.json.get("solution")]
    if not all(data):
        return {
            "message" : "enter all information"
        }
    res = CSubmission.submit_code(*data)
    print(res)
    if res:
        return res,200
    return{
            "message" : "unknown error"
        },500

@Submission.get("/mysubmissions")
def view_submissions():
    uid = session.get("uid")
    if not uid:
        return {
            "message" : "login required"
        }
    return CSubmission.get_submissions(uid)

@Submission.get("/all")
def view_all_submissions():
    return CSubmission.get_all_submissions()
