from datetime import datetime
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class StaffDetails(BaseModel):
    """
    Contains details about staff involved in the schedule.
    """

    id: int
    userId: int
    user: prisma.models.User


class Field(BaseModel):
    """
    Information regarding the field where the activity is scheduled
    """

    id: int
    name: str
    condition: prisma.enums.FieldCondition
    mapUrl: str


class ScheduleDetailsResponse(BaseModel):
    """
    Response model contains detailed information of the schedule including the related activities, resources (like fields involved) and any notes from staff.
    """

    id: int
    date: datetime
    activityType: prisma.enums.ActivityType
    staffDetails: Optional[StaffDetails] = None
    fieldDetails: Optional[Field] = None
    notes: Optional[str] = None


async def getScheduleById(scheduleId: int) -> ScheduleDetailsResponse:
    """
    Retrieves detailed information about a specific schedule by scheduleId. This includes all details like associated date, time, activity, involved resources or fields, and any pertinent notes or updates from staff.

    Args:
        scheduleId (int): Unique identifier of the Schedule to retrieve the details for.

    Returns:
        ScheduleDetailsResponse: Response model contains detailed information of the schedule including the related activities,
                                 resources (like fields involved) and any notes from staff.
    """
    schedule = await prisma.models.Schedule.prisma().find_unique(
        where={"id": scheduleId},
        include={"staffDetails": {"include": {"user": True}}, "field": True},
    )
    if not schedule:
        raise ValueError(f"Schedule with ID {scheduleId} not found")
    staff_details = (
        Field(
            id=schedule.staffDetails.id,
            userId=schedule.staffDetails.userId,
            user=prisma.models.User(
                id=schedule.staffDetails.user.id,
                email=schedule.staffDetails.user.email,
                hashedPassword=schedule.staffDetails.user.hashedPassword,
                role=schedule.staffDetails.user.role,
            ),
        )
        if schedule.staffDetails
        else None
    )  # TODO(autogpt): Arguments missing for parameters "name", "condition", "mapUrl". reportCallIssue
    field_details = (
        Field(
            id=schedule.field.id,
            name=schedule.field.name,
            condition=schedule.field.condition,
            mapUrl=schedule.field.mapUrl,
        )
        if schedule.field
        else None
    )
    return ScheduleDetailsResponse(
        id=schedule.id,
        date=schedule.date,
        activityType=schedule.activityType,
        staffDetails=staff_details,
        fieldDetails=field_details,
        notes=None,
    )
