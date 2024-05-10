from datetime import datetime, timedelta

import prisma
import prisma.enums
import prisma.models
from jose import jwt
from passlib.hash import bcrypt
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Response payload for a successful login. Contains the JWT, user's role, and user ID.
    """

    jwt: str
    role: prisma.enums.Role
    userId: int


async def authenticateUser(username: str, password: str) -> LoginResponse:
    """
    Handles user authentication. Expects username and password in the request body.
    Returns a JSON Web Token (JWT) for session handling on successful authentication,
    along with user role and ID for role-based access throughout the app.

    Args:
        username (str): The username of the user trying to log in.
        password (str): The password of the user. This must be handled securely.

    Returns:
        LoginResponse: Response payload for a successful login. Contains the JWT, user's role, and user ID.

    Raises:
        ValueError: If authentication fails for any reason, such as wrong password or non-existent user.

    Example:
        response = authenticateUser('johnDoe', 's3cr3tPassword')
        print(response)
        > {
            'jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX...',
            'role': prisma.enums.Role.Staff,
            'userId': 15
        }
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user is None or not bcrypt.verify(password, user.hashedPassword):
        raise ValueError("Invalid username or password")
    expiration_time = datetime.utcnow() + timedelta(days=1)
    token_data = {"sub": user.id, "role": user.role, "exp": expiration_time}
    secret_key = "your_secret_key"
    algorithm = "HS256"
    jwt_token = jwt.encode(token_data, secret_key, algorithm=algorithm)
    return LoginResponse(jwt=jwt_token, role=user.role, userId=user.id)
