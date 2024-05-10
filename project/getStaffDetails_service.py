from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Schedule(BaseModel):
    """
    Represents an event or task scheduled on a specific date, for specific activityType and resources, at a specific Field location.
    """

    id: int
    date: datetime
    activityType: prisma.enums.ActivityType
    staffDetailsId: int
    fieldId: Optional[int] = None


class StaffMemberDetailedInfo(BaseModel):
    """
    Detailed data model encapsulating user, payroll, schedule, and reviews data.
    """

    user: prisma.models.User
    payroll: prisma.models.Payroll
    schedules: List[Schedule]
    reviews: List[prisma.models.Review]


class StaffDetailsResponse(BaseModel):
    """
    Response model returning the detailed information of a staff member including linked payroll, schedules, and performance reviews.
    """

    staffDetails: StaffMemberDetailedInfo


async def getStaffDetails(id: int) -> StaffDetailsResponse:
    """
    Fetches detailed information of a single staff member using their ID. Only accessible to Admin, HR,
    and to the individual staff member when retrieving their own details.

    Args:
        id (int): Unique identifier of the staff member to fetch the details for.

    Returns:
        StaffDetailsResponse: Response model returning the detailed information of a staff member including linked payroll,
                              schedules, and performance reviews.

    Raises:
        ValueError: If no staff details or associated user is found for the given ID.
    """
    staff_details = await prisma.models.StaffDetails.prisma().find_unique(
        where={"id": id},
        include={"user": True, "payroll": True, "reviews": True, "schedules": True},
    )
    if staff_details is None:
        raise ValueError("No staff details found for ID: {}".format(id))
    if staff_details.user is None:
        raise ValueError(
            "No user associated with the staff details for ID: {}".format(id)
        )
    detailed_info = StaffMemberDetailedInfo(
        user=staff_details.user,
        payroll=staff_details.payroll,
        schedules=staff_details.schedules,
        reviews=staff_details.reviews,
    )
    return StaffDetailsResponse(staffDetails=detailed_info)
