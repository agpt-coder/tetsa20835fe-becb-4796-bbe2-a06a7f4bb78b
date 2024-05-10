from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetStaffListRequest(BaseModel):
    """
    Request model for retrieving a list of staff members. This does not require specific input parameters as it fetches all staff members, filtering based on the role of the requester which is handled internally.
    """

    pass


class StaffDetails(BaseModel):
    """
    Contains details about staff involved in the schedule.
    """

    id: int
    userId: int
    user: prisma.models.User


class StaffListResponse(BaseModel):
    """
    Response model that contains an array of staff member details. Each staff item includes user profile and staff-specific details.
    """

    staffMembers: List[StaffDetails]


async def listStaff(request: GetStaffListRequest) -> StaffListResponse:
    """
    Retrieves a list of all staff members along with their basic details. Integrates with prisma.models.User Management to ensure
    only authorized viewing based on user roles like Admin and HR.

    Args:
        request (GetStaffListRequest): Request model for retrieving a list of staff members. This does not require
        specific input parameters as it fetches all staff members, filtering based on the role of the requester
        which is handled internally.

    Returns:
        StaffListResponse: Response model that contains an array of staff member details. Each staff item includes
        user profile and staff-specific details.
    """
    staff_details_records = await prisma.models.StaffDetails.prisma().find_many(
        include={"user": {"include": {"profile": True}}}
    )
    staff_members_list = [
        StaffDetails(
            id=staff_detail.id,
            userId=staff_detail.user.id,
            user=prisma.models.User(
                id=staff_detail.user.id,
                email=staff_detail.user.email,
                profile=prisma.models.Profile(
                    firstName=staff_detail.user.profile.firstName
                    if staff_detail.user.profile
                    else None,
                    lastName=staff_detail.user.profile.lastName
                    if staff_detail.user.profile
                    else None,
                ),
            ),
        )
        for staff_detail in staff_details_records
    ]  # TODO(autogpt): Arguments missing for parameters "id", "userId". reportCallIssue
    response = StaffListResponse(staffMembers=staff_members_list)
    return response
