from flask import Blueprint, jsonify, session, request
from Application.controller import CProblems

Problems = Blueprint("problems","problems")

@Problems.post('/create')
def create_problem():
    if session.get("user") != "Admin":
        return {
            "message" : "unauthorised"
        },403
    que = [request.json.get("pname"),request.json.get("pdesc"),request.json.get("code"),request.json.get("tb")]
    res = CProblems.create_problem(*que)
    if res == "invalid":
        return {
            "message" : "something wrong in code/tb"
        },406
    elif res == "created":
        return {
            "message" : "created",
            "generated output" : res
        },201
    return {
        "message" : "unknown error"
    },500

@Problems.patch('/edit')
def edit_problem():
    if session.get("user") != "Admin":
        return {
            "message" : "unauthorised"
        },403
    pid = request.json.get("pid")
    if not pid:
        return {
            "message" : "input pid"
        },400
    temp = dict(request.json)
    temp.pop("pid")
    res = CProblems.edit_problem(pid,**temp)
    if res:
        return res
    return {
            "message" : "unknown error"
    },500

@Problems.get('/all')
def view_problem():
    res = CProblems.view_problems()
    if res or res == []:
        return jsonify(res)
    return  {
        "message" : "unknown error"
    },500

@Problems.delete('/delete')
def delete_problem():
    if session.get("user") != "Admin":
        return {
            "message" : "unauthorised"
        },403
    pid = request.json.get("pid")
    if not pid:
        return {
            "message" : "input pid"
        },400
    if CProblems.delete_problem(pid):
        return {
            "message" : "deleted"
        },200
    return {
            "message" : "unknown error"
        },500

@Problems.post('/add')
def add_problem():
    pid = request.json.get("pid")
    cid = request.json.get("cid")
    if session.get("user") != "Admin":
        return {
            "message" : "unauthorised"
        },403
    if not pid or not cid:
        return {
            "message" : "input pid and cid"
        },400
    if CProblems.add_problem(cid,pid):
        return {
            "message" : "added"
        },201
    return {
        "message" : "unknown error"
    },500
@Problems.delete('/remove')
def remove_problem():
    pid = request.json.get("pid")
    cid = request.json.get("cid")
    if session.get("user") != "Admin":
        return {
            "message" : "unauthorised"
        },403
    if not pid or not cid:
        return {
            "message" : "input pid and cid"
        },400
    res = CProblems.remove_problem(cid,pid)
    if res:
        return {
            "message" : "removed"
        },204
    return {
        "message" : "unknown error"
    },500