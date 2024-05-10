from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class AddStaffResponse(BaseModel):
    """
    Response provided after successfully adding a new staff member. Includes the ID of the newly created staff profile as a confirmation.
    """

    success: bool
    staffId: int
    message: str


class Role(BaseModel):
    """
    Enumeration of staff roles provided as a model.
    """

    staffType: str


async def addStaff(
    firstName: str,
    lastName: str,
    email: str,
    phone: Optional[str],
    role: Role,
    hashedPassword: str,
) -> AddStaffResponse:
    """
    Adds a new staff member to the system. Requires input of personal details, role, and permissions. Ensures data consistency through validations and role checking with User Management.

    Args:
        firstName (str): First name of the staff member.
        lastName (str): Last name of the staff member.
        email (str): Email address of the staff member. Must be unique across the system.
        phone (Optional[str]): Phone number of the staff member, optional.
        role (Role): Role of the staff member which defines their permissions and access within the system.
        hashedPassword (str): Securely hashed password for the staff member to log in to the system.

    Returns:
        AddStaffResponse: Response provided after successfully adding a new staff member. Includes the ID of the newly created staff profile as a confirmation.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return AddStaffResponse(
            success=False, staffId=0, message="Email already in use."
        )
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "hashedPassword": hashedPassword,
            "role": role,
            "profile": {
                "create": {"firstName": firstName, "lastName": lastName, "phone": phone}
            },
        }
    )
    if user:
        return AddStaffResponse(
            success=True, staffId=user.id, message="Staff member added successfully."
        )
    else:
        return AddStaffResponse(
            success=False,
            staffId=0,
            message="An error occurred while adding the staff member.",
        )
