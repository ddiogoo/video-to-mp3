"""
This module provides functionality to validate authentication tokens by  communicating with an external authentication service.
"""

import os, requests

from flask import Request


def token(request: Request) -> (tuple[None, tuple[str, int]] | tuple[str, None]):
    """
    Validates the authorization token from the incoming request.

    This function checks for the presence of an "Authorization" header in the request.
    If the header is missing or the token is empty, it returns an error message and 
    an HTTP status code of 401. Otherwise, it forwards the token to an external 
    authentication service for validation.

    Args:
        request (Request): The incoming HTTP request containing headers.

    Returns:
        tuple[None, tuple[str, int]]: If validation fails, returns None and a tuple 
        containing an error message and the HTTP status code.
        tuple[str, None]: If validation succeeds, returns the validated token as a 
        string and None for the error.
    """
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)
    token = request.headers["Authorization"]
    if not token:
        return None, ("missing credentials", 401)
    response = requests.post(f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate", 
                             headers={"Authorization": token})
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    