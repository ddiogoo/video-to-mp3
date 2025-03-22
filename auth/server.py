"""
This python file is the server that will be used to authenticate users.
The server will be responsible for authenticating users and generating JWT tokens.
The server will be connected to a MySQL database to store user information.
"""

import jwt, datetime, os

from dotenv import load_dotenv
from flask import Flask, request
from flask_mysqldb import MySQL

load_dotenv()
server = Flask(__name__)
mysql = MySQL(server)

server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
server.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
        
        
def create_jwt(email, secret, authz):
    """
    Function to create a JWT token for a user.

    Args:
        email (str): The email of the user.
        secret (str): The secret key to sign the JWT token.
    """
    return jwt.encode(
        {
            "username": email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "admin": authz,
        },
        secret, 
        algorithm="HS256",
    )
 

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 400
    
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email, password FROM user WHERE email = %s", (auth.username,))
    if res <= 0:
        return "invalid credentials", 401
    
    user_row = cur.fetchone()
    email = user_row[0]
    password = user_row[1]
    
    if auth.username != email or auth.password != password:
        return "invalid credentials", 401
    return create_jwt(auth.username, os.environ.get('JWT_SECRET'), True)


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
