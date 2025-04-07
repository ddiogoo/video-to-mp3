"""
This python file is the main entry point for the Flask application.
"""

import json
import os, gridfs, pika

from auth import validate
from auth_svc import access
from dotenv import load_dotenv
from flask import Flask, request
from flask_pymongo import PyMongo


load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI_CONNECTION")

mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

connParameters = os.environ.get("RABBITMQ_CONNECTION_PARAMETERS")
connection = pika.BlockingConnection(pika.ConnectionParameters(connParameters))
channel = connection.channel()


@app.route("/login", method=["POST"])
def login():
    """
    This function is used to login a user. 
    It takes the request object as an argument and returns a token if the login is successful. 
    If the login fails, it returns an error message.

    Returns:
        token: str or None
            The token returned by the auth service if the login is successful.
        err: tuple or None
            An error message if the login fails.
    """
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    if err:
        return err
    access = json.loads(access)
    if access["admin"]:
        if len(request.files) != 1:
            return "Exactly one file is required", 400
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)
            if err:
                return err
        return "success!", 200
    else:
        return "not authorized", 401
