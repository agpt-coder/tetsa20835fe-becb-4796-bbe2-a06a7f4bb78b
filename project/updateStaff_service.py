from enum import Enum
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class StaffDetails(BaseModel):
    """
    Contains details about staff involved in the schedule.
    """

    id: int
    userId: int
    user: prisma.models.User


class StaffUpdateResponse(BaseModel):
    """
    Returns updated details of the staff member after successful edit. Includes any system-generated messages or acknowledgments.
    """

    successful: bool
    message: str
    updated_staff_details: StaffDetails


class Role(Enum):
    Admin: str = "Admin"
    Staff: str = "Staff"
    Manager: str = "Manager"
    Accountant: str = "Accountant"
    HR: str = "HR"
    FieldWorker: str = "FieldWorker"


async def updateStaff(
    id: int, email: str, firstName: str, lastName: str, phone: Optional[str], role: Role
) -> StaffUpdateResponse:
    """
    Updates the details of an existing staff member. Only Admin and HR can edit roles and permissions,
    while self-update is limited to personal information by the staff themselves.

    Args:
        id (int): The ID of the staff member to update. This is used to identify the record in the database.
        email (str): The new email address of the staff member, if applicable.
        firstName (str): The first name of the staff member.
        lastName (str): The last name of the staff member.
        phone (Optional[str]): The updated phone number of the staff member, if provided.
        role (Role): The new role for the staff member, changeable only by Admin and HR roles.

    Returns:
        StaffUpdateResponse: Returns updated details of the staff member after successful edit. Includes any system-generated messages or acknowledgments.
    """
    current_user = await prisma.models.User.prisma().find_unique(
        where={"id": "CURRENT_USER_ID"}
    )
    if not current_user or current_user.role not in [Role.Admin, Role.HR]:
        return StaffUpdateResponse(
            successful=False,
            message="Unauthorized to change the role.",
            updated_staff_details=None,
        )
    target_user = await prisma.models.User.prisma().find_unique(where={"id": id})
    if not target_user:
        return StaffUpdateResponse(
            successful=False,
            message="No staff member found with given ID.",
            updated_staff_details=None,
        )
    await prisma.models.User.prisma().update(
        where={"id": id}, data={"email": email, "role": role}
    )
    await prisma.models.Profile.prisma().update(
        where={"userId": id},
        data={"firstName": firstName, "lastName": lastName, "phone": phone},
    )
    updated_user = await prisma.models.User.prisma().find_unique(where={"id": id})
    if updated_user is None:
        return StaffUpdateResponse(
            successful=False,
            message="Failed to fetch updated user details.",
            updated_staff_details=None,
        )
    staff_details = StaffDetails(
        id=updated_user.id, userId=updated_user.id, user=updated_user
    )
    return StaffUpdateResponse(
        successful=True,
        message="Staff member details updated successfully.",
        updated_staff_details=staff_details,
    )
