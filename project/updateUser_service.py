from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class UpdatedUserInfo(BaseModel):
    """
    This model returns the updated information of the user after successful update operation.
    """

    userId: int
    email: str
    firstName: str
    lastName: str
    role: str


class Role(Enum):
    Admin: str = "Admin"
    Staff: str = "Staff"
    Manager: str = "Manager"
    Accountant: str = "Accountant"
    HR: str = "HR"
    FieldWorker: str = "FieldWorker"


async def updateUser(
    userId: int, email: str, firstName: str, lastName: str, role: Role
) -> UpdatedUserInfo:
    """
    Updates user information such as email, name, or role. Requires user ID in the path and updated data fields in the request body.
    Returns updated information of the user. Ensures that sensitive changes like role updates are logged for security compliance.

    Args:
        userId (int): The unique identifier of the user to be updated.
        email (str): The new email address of the user.
        firstName (str): The user's first name.
        lastName (str): The user's last name.
        role (Role): The new role assigned to the user. Changes should be logged for compliance.

    Returns:
        UpdatedUserInfo: This model returns the updated information of the user after successful update operation.

    Example:
        updateUser(1, 'new.email@example.com', 'Updated', 'User', Role.Staff)
        > UpdatedUserInfo(userId=1, email='new.email@example.com', firstName='Updated', lastName='User', role='Staff')
    """
    old_user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if old_user.role != role:
        print(f"Change of role for user {userId} from {old_user.role} to {role}")
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId},
        data={
            "email": email,
            "role": role,
            "profile": {"update": {"firstName": firstName, "lastName": lastName}},
        },
        include={"profile": True},
    )
    if not updated_user:
        raise ValueError(f"No user found for ID {userId}")
    return UpdatedUserInfo(
        userId=updated_user.id,
        email=updated_user.email,
        firstName=updated_user.profile.firstName if updated_user.profile else "",
        lastName=updated_user.profile.lastName if updated_user.profile else "",
        role=updated_user.role,
    )
