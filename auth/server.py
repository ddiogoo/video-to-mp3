"""
This python file is the server that will be used to authenticate the user.
"""

import jwt, os

from dotenv import load_dotenv
from flask import Flask, request
from database.database import User, db
from utils.jwt import create_jwt


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI_CONNECTION")
db.init_app(app)


@app.route("/register", methods=["POST"])
def register():
    """
    Register the user.

    Returns:
        str, int: The success message (Or an error message) and the status code.
    """
    user = request.get_json()
    if not user:
        return "invalid credentials", 400
    
    newUser = User(**user)
    try:
        db.session.add(newUser)
        db.session.commit()
        return "User created", 201
    except:
        db.session.rollback()
        return "User already exists", 400


@app.route("/login", methods=["POST"])
def login():
    """
    Login the user.

    Returns:
        str, int: The JWT token (Or an error message) and the status code.
    """
    auth = request.authorization
    if not auth:
        return "missing credentials", 400
    
    user = db.session.query(User).filter(User.email == auth.username).first()
    if not user:
        return "User not found", 404
    
    if auth.username != user.email or auth.password != user.password:
        return "invalid credentials", 401
    return create_jwt(user.email, os.environ.get('JWT_SECRET'), True)


@app.route("/validate", methods=["POST"])
def validate():
    """
    Validate the user.

    Returns:
        str, int: The success message (Or an error message) and the status code.
    """
    encode_token = request.headers["Authorization"]
    if not encode_token:
        return "missing token", 400
    encode_token = encode_token.split(" ")[1]
    try:
        jwt.decode(encode_token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "expired token", 401
    except jwt.InvalidTokenError:
        return "invalid token", 401
    return "valid token", 200


if __name__ == "__main__":
    """
    Run the server.

    Raises:
        e: An exception if the db cannot create all the tables.
    """
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        raise e.args
    app.run(host="0.0.0.0", port=5000)
