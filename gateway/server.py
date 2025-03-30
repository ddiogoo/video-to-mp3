import os, gridfs, pika

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
