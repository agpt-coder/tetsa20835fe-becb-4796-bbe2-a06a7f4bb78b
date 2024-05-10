from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ScheduleActivityDetails(BaseModel):
    """
    Detail structure for activities scheduled on the field.
    """

    activityType: prisma.enums.ActivityType
    date: datetime
    staffDetailsId: int


class FieldDetailsResponse(BaseModel):
    """
    Response model containing detailed information about the field, including activities scheduled, soil type, and crop status. This will assist staff in managing and monitoring field assignments efficiently.
    """

    fieldId: int
    name: str
    mapUrl: str
    areaSize: float
    condition: prisma.enums.FieldCondition
    activities: List[ScheduleActivityDetails]


async def getFieldDetails(fieldId: int) -> FieldDetailsResponse:
    """
    Fetches details of a specific field including soil type, crop status, and recent activities by passing fieldId.
    Useful for monitoring and deploying field workers as per requirements.

    Args:
        fieldId (int): The unique identifier for the field whose details are being requested.

    Returns:
        FieldDetailsResponse: Response model containing detailed information about the field, including activities scheduled, soil type, and crop status. This will assist staff in managing and monitoring field assignments efficiently.

    Example:
        field_details = await getFieldDetails(1)
        > FieldDetailsResponse(fieldId=1, name='Northfield', mapUrl='http://maps.example.com/field/1', areaSize=20.0, condition='Healthy', activities=[...])
    """
    field = await prisma.models.Field.prisma().find_unique(
        where={"id": fieldId},
        include={"activities": {"include": {"staffDetails": True}}},
    )  # TODO(autogpt): "Field" is not exported from module "prisma.models". reportPrivateImportUsage
    if field is None:
        raise ValueError(f"No field found with ID {fieldId}.")
    activities = [
        ScheduleActivityDetails(
            activityType=activity.activityType.name,
            date=activity.date,
            staffDetailsId=activity.staffDetails.user.profile.userId,
        )
        if activity.staffDetails
        and activity.staffDetails.user
        and activity.staffDetails.user.profile
        else None
        for activity in field.activities
    ]
    return FieldDetailsResponse(
        fieldId=field.id,
        name=field.name,
        mapUrl=field.mapUrl,
        areaSize=field.areaSize,
        condition=field.condition.name,
        activities=activities,
    )
