from flask import Blueprint, make_response, session, request
from Application.controller import CAuth

Auth = Blueprint("auth","auth")

@Auth.get('/status')
def auth_status():
    return {
        "message" : {
            "user" : session.get("user")
        }
    },200

@Auth.post('/login')
def login():
    uname = request.json.get("uname")
    passwd = request.json.get("passwd")
    valid = CAuth.validate_password(uname,passwd)
    if valid:
        session["user"] = uname
        session["uid"] = valid[1]
        response = make_response({
            "message" : "login successful"
        },200)
        print(dict(session))
        return response
    return {
            "message" : "login failed"
        },403


@Auth.post('/signup')
def signup():
    uname = request.json.get("uname")
    passwd = request.json.get("passwd")
    if not uname or not passwd:
        return {
            "message" : "enter uname/passwd"
        },400

    if CAuth.create_user(uname,passwd):
        return {
            "message" : "created"
        },200
    return {
            "message" : "failed"
        },406

@Auth.post('/logout')
def logout():
    if session.get("user"):
        session.pop("user",None)
        session.pop("uid",None)
    return {
        "logout" : True
    },200


