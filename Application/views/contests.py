from flask import Blueprint, session, request
from Application.controller import CContest

Contest = Blueprint("contest","contest")

@Contest.get('/')
def all_contests():
    return CContest.list_all(),200

@Contest.post('/enroll')
def contest_enroll():
    if not session.get("user"):
        return {
            "message" : "login required"
        }, 403
    cid = request.json.get("cid")
    if not cid:
        return {
            "message" : "enter contest id(cid)"
        },400
    if CContest.contest_enroll(session["uid"],cid):
        return {
            "message" : "enrolled"
        },200
    
    return {
            "message" : "unknown error"
        },500

@Contest.post('/create')
def create_contest():
    if not session.get("user"):
        return {
            "message" : "login required"
        },403
    cname = request.json.get("cname")
    if not cname:
        return {
            "message" : "enter contest name(cname)"
        },400
    if CContest.create_contest(cname):
        return {
            "message" : "created"
        },201
    
    return {
            "message" : "unknown error"
        },500
