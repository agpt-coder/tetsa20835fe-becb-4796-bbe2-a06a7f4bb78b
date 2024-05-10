from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetSchedulesRequest(BaseModel):
    """
    Defines the parameters for requesting a list of all scheduling events. It could also include optional query parameters for filtering (such as by date range or activity type), but here, we're starting with a simple request that retrieves all data.
    """

    pass


class FieldInfo(BaseModel):
    """
    Details of the field related to a schedule.
    """

    id: int
    name: str
    condition: prisma.enums.FieldCondition
    mapUrl: str


class ScheduleDetail(BaseModel):
    """
    Detailed information for each schedule event, including linked field condition.
    """

    id: int
    date: datetime
    activityType: prisma.enums.ActivityType
    field: FieldInfo


class GetSchedulesResponse(BaseModel):
    """
    Provides a detailed response containing a list of scheduling events, including details about the dates, activities, and fields involved.
    """

    schedules: List[ScheduleDetail]


async def getSchedules(request: GetSchedulesRequest) -> GetSchedulesResponse:
    """
    Retrieves a list of all scheduling events, including planting, harvesting, and delivery schedules.
    Each schedule entry contains relevant details such as date, time, activity type, and related field
    location or resources involved. This endpoint also utilizes information from the Mapping and
    Field Management module to provide context on field conditions.

    Args:
        request (GetSchedulesRequest): Defines the parameters for requesting a list of all scheduling events.

    Returns:
        GetSchedulesResponse: Provides a detailed response containing a list of scheduling events,
                              including details about the dates, activities, and fields involved.
    """
    schedules = await prisma.models.Schedule.prisma().find_many(include={"field": True})
    details_list = []
    for schedule in schedules:
        if schedule.field:
            field_info = FieldInfo(
                id=schedule.field.id,
                name=schedule.field.name,
                condition=schedule.field.condition.name,
                mapUrl=schedule.field.mapUrl,
            )
        else:
            field_info = FieldInfo(
                id=-1,
                name="No field assigned",
                condition="Unknown",
                mapUrl="No URL provided",
            )
        detail = ScheduleDetail(
            id=schedule.id,
            date=schedule.date,
            activityType=schedule.activityType.name,
            field=field_info,
        )
        details_list.append(detail)
    return GetSchedulesResponse(schedules=details_list)
