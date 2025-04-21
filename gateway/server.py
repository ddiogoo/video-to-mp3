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
from storage import util


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
    Handles the login functionality for the application.

    This route listens for POST requests at the "/login" endpoint. It uses the 
    `access.login` method to authenticate the user based on the request data. 
    If authentication is successful, it returns a token. Otherwise, it returns 
    an error message.

    Returns:
        str: A token if authentication is successful.
        str: An error message if authentication fails.
    """
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@app.route("/upload", methods=["POST"])
def upload():
    """
    Handles file upload requests to the "/upload" endpoint.

    This function validates the user's access token, checks if the user has 
    admin privileges, and processes the uploaded file. Only one file is 
    allowed per request.

    Returns:
        - If the access token is invalid or the user is not authorized:
        A tuple containing an error message and the appropriate HTTP status code.
        - If the user is authorized but the request does not contain exactly one file:
        A tuple with an error message and a 400 status code.
        - If the file upload is successful:
        A success message with a 200 status code.
        - If an error occurs during file upload:
        The error message returned by the `util.upload` function.

    Request:
        - Headers:
            - Authorization: Bearer token for user authentication.
        - Files:
            - Exactly one file to be uploaded.

    Dependencies:
        - `validate.token`: Validates the user's access token.
        - `util.upload`: Handles the file upload process.
        - `fs`, `channel`: External resources used during the upload process.

    Notes:
        - Only users with admin privileges are authorized to upload files.
        - The function expects the access token to be a JSON object with an 
        "admin" key indicating the user's privileges.
    """
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


@app.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
