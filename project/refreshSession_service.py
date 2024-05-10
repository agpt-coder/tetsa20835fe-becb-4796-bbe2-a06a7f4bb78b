from datetime import datetime, timedelta
from os import getenv

import jwt
from pydantic import BaseModel


class AuthRefreshResponse(BaseModel):
    """
    Model to return a new JWT after the previous token was validated. Ensures continuous user session without re-login.
    """

    newToken: str


def refreshSession(Authorization: str) -> AuthRefreshResponse:
    """
    Refreshes the authentication session by issuing a new token. Requires a valid JWT in the request header. Helps maintain user session continuity safely.

    Args:
        Authorization (str): The JWT used for verifying the user's current session. This token should be included in the request headers.

    Returns:
        AuthRefreshResponse: Model to return a new JWT after the previous token was validated. Ensures continuous user session without re-login.

    Raises:
        Exception: If the token is invalid, expired, or nearing expiry.
    """
    SECRET_KEY = getenv("JWT_SECRET_KEY", "")
    try:
        decoded_token = jwt.decode(Authorization, SECRET_KEY, algorithms=["HS256"])
        new_jwt_payload = {
            "user_id": decoded_token.get("user_id"),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        new_token = jwt.encode(new_jwt_payload, SECRET_KEY, algorithm="HS256")
        return AuthRefreshResponse(newToken=new_token)
    except jwt.ExpiredSignatureError:
        raise Exception("The provided token has expired.")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token provided.")
