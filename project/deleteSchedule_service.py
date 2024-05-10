from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteScheduleResponse(BaseModel):
    """
    Response model following the deletion of a schedule. Primarily indicates success of the deletion process and potentially could return details of resources updated due to deletion.
    """

    success: bool
    updated_field_ids: List[int]
    message: str


async def deleteSchedule(scheduleId: int) -> DeleteScheduleResponse:
    """
    Deletes a schedule identified by the scheduleId. This action removes the schedule from the system and updates related resource allocations and field statuses accordingly.

    Args:
        scheduleId (int): Unique identifier for the schedule to be deleted. Must exist in the schedules database table.

    Returns:
        DeleteScheduleResponse: Response model following the deletion of a schedule. Primarily indicates success of the deletion process and potentially could return details of resources updated due to deletion.
    """
    schedule = await prisma.models.Schedule.prisma().find_unique(
        where={"id": scheduleId}, include={"field": True}
    )
    if schedule is None:
        return DeleteScheduleResponse(
            success=False,
            updated_field_ids=[],
            message="Schedule with the provided ID does not exist.",
        )
    field_update_ids = []
    if schedule.field:
        field_id = schedule.field.id
        await prisma.models.Schedule.prisma().update(
            where={"id": scheduleId},
            data={"field": {"update": {"condition": "NeedsAttention"}}},
        )
        field_update_ids.append(field_id)
    await prisma.models.Schedule.prisma().delete(where={"id": scheduleId})
    return DeleteScheduleResponse(
        success=True,
        updated_field_ids=field_update_ids,
        message="Successfully deleted the schedule and updated associated resources.",
    )
