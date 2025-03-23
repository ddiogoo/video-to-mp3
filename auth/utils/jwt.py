"""
This python module is to create utility functions.
"""

import datetime
import jwt


def create_jwt(email, secret, authz) -> str:
    """
    Create a JWT token for the user.

    Args:
        email (str): The email of the user.
        secret (str): The secret key to encode the JWT.
        authz (str): The authorization of the user.

    Returns:
        str: The JWT token.
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
