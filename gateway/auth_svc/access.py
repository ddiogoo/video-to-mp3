"""
This module handles the authentication of users.
It uses the requests library to send a POST request to the authentication service to verify the user's credentials.
"""

import os, requests


def login(request):
    """
    This function handles the login process for the user.
    It retrieves the user's credentials from the request and sends them to the authentication service.
    If the credentials are valid, it returns the user's token.

    Args:
        request: The request object containing the user's credentials.

    Returns:
        tuple: A tuple containing the user's token and an error message if applicable.
    """
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)
    basicAuth = (auth.username, auth.password)
    response = requests.post(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth)
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    