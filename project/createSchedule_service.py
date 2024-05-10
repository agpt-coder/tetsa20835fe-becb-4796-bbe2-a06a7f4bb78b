from datetime import datetime
from enum import Enum
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ScheduleCreationResponse(BaseModel):
    """
    Response after trying to create a scheduling event. Provides schedule ID if successful and relevant messages or errors.
    """

    success: bool
    scheduleId: Optional[int] = None
    message: str


class ActivityType(Enum):
    Planting: str = "Planting"
    Harvesting: str = "Harvesting"
    Delivery: str = "Delivery"


async def createSchedule(
    date: datetime,
    activityType: ActivityType,
    staffDetailsId: Optional[int],
    fieldId: Optional[int],
    inventoryItemId: Optional[int],
) -> ScheduleCreationResponse:
    """
    Creates a new scheduling event. Requires details such as date, time, type of activity (planting, harvesting, delivery),
    and associated resources or locations. The system checks for field availability and resource constraints by interacting
    with the Mapping and Field Management and Supply Chain Management modules before confirming the creation of the schedule.

    Args:
        date (datetime): The scheduled date for the activity.
        activityType (ActivityType): The type of activity scheduled, such as Planting, Harvesting, or Delivery.
        staffDetailsId (Optional[int]): Links the schedule to the staff member details if needed, optional.
        fieldId (Optional[int]): The field where the activity is to occur. Optional, as not all activities need a designated field.
        inventoryItemId (Optional[int]): Item from inventory linked to the activity, such as tools or vehicles. Optional as not all activities will require inventory items.

    Returns:
        ScheduleCreationResponse: Response after trying to create a scheduling event. Provides schedule ID if successful
        and relevant messages or errors.
    """
    if staffDetailsId is not None:
        staff_details = await prisma.models.StaffDetails.prisma().find_unique(
            where={"id": staffDetailsId}
        )
        if staff_details is None:
            return ScheduleCreationResponse(
                success=False, message="Staff details not found for provided ID."
            )
    if inventoryItemId is not None:
        inventory_item = await prisma.models.InventoryItem.prisma().find_unique(
            where={"id": inventoryItemId}
        )
        if inventory_item is None:
            return ScheduleCreationResponse(
                success=False, message="Inventory item not found for provided ID."
            )
        elif inventory_item.status == prisma.enums.InventoryStatus.OutOfStock:
            return ScheduleCreationResponse(
                success=False, message="Inventory item is out of stock."
            )
    schedule_data = {
        "date": date,
        "activityType": activityType,
        "staffDetailsId": staffDetailsId,
        "fieldId": fieldId,
    }
    new_schedule = await prisma.models.Schedule.prisma().create(data=schedule_data)
    return ScheduleCreationResponse(
        success=True,
        scheduleId=new_schedule.id,
        message="Schedule created successfully.",
    )
