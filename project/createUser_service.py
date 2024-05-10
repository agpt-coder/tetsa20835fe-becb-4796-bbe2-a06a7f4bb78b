from enum import Enum

import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Response model returning basic user information after successful account creation.
    """

    userId: int
    username: str
    email: str
    role: prisma.enums.Role


class Role(Enum):
    Admin: str = "Admin"
    Staff: str = "Staff"
    Manager: str = "Manager"
    Accountant: str = "Accountant"
    HR: str = "HR"
    FieldWorker: str = "FieldWorker"


async def createUser(username: str, email: str, password: str) -> CreateUserResponse:
    """
    Creates a new user account by taking user details - username, email, and raw password, and hashing the password before storing
    it in the database. Assigns a default role of 'Staff' to the user account. Returns the created user's ID, username, email, and role back to the caller.

    Args:
        username (str): The desired username for the new account.
        email (str): Email address for the new user account, used for login and communication.
        password (str): Raw password that will be hashed before storage.

    Returns:
        CreateUserResponse: Response model returning basic user information after successful account creation.

    Example:
        response = await createUser("john_doe", "john.doe@example.com", "securepassword123")
        print(response)
        > CreateUserResponse(userId=1, username='john_doe', email='john.doe@example.com', role='Staff')
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "hashedPassword": hashed_password,
            "role": prisma.enums.Role.Staff,
        }
    )
    response = CreateUserResponse(
        userId=user.id, username=username, email=user.email, role=user.role
    )
    return response
