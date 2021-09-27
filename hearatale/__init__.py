from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, current_user

app = Flask(__name__)
app.config.from_object('config')

jwt = JWTManager(app)

db = SQLAlchemy(app)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/student/login", methods=["POST"])
def slogin():
    password = request.json.get("password", None)

    s = Student.login(password)
    if not s:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=s.uuid)
    return jsonify(access_token=access_token)


@app.route("/teacher/login", methods=["POST"])
def tlogin():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    t = Teacher.login(username, password)
    if not t:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=t.uuid)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    return jsonify(logged_in_as=current_user.uuid), 200

from models import *
