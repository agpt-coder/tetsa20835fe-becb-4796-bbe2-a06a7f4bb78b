from enum import Enum
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    Response model comprising the user’s detailed information for public profile viewing, excluding any sensitive data such as passwords.
    """

    id: int
    email: str
    firstName: str
    lastName: str
    phone: Optional[str] = None
    role: prisma.enums.Role


class Role(Enum):
    Admin: str = "Admin"
    Staff: str = "Staff"
    Manager: str = "Manager"
    Accountant: str = "Accountant"
    HR: str = "HR"
    FieldWorker: str = "FieldWorker"


async def getUser(userId: str) -> UserProfileResponse:
    """
    Retrieves a user's profile based on the provided user ID. Returns the user’s detailed information,
    excluding sensitive data like passwords. Useful for profile viewing and management operations.

    Args:
        userId (str): The unique identifier of the user. This is used to fetch the correct profile from the database.

    Returns:
        UserProfileResponse: Response model comprising the user’s detailed information for public profile viewing,
                             excluding any sensitive data such as passwords.

    Example:
        getUser('123')
        > UserProfileResponse(id=123, email='user@example.com', firstName='Jane', lastName='Doe', phone='1234567890', role=prisma.enums.Role.Staff)
    """
    user_record = await prisma.models.User.prisma().find_unique(
        where={"id": int(userId)}, include={"profile": True}
    )
    if not user_record:
        raise ValueError("User not found")
    profile = user_record.profile
    if not profile:
        raise ValueError("Profile not found for user")
    return UserProfileResponse(
        id=user_record.id,
        email=user_record.email,
        firstName=profile.firstName,
        lastName=profile.lastName,
        phone=profile.phone,
        role=prisma.enums.Role[user_record.role],
    )
