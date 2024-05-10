from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetSupplyChainItemsRequest(BaseModel):
    """
    Request model for fetching all inventory items in the supply chain. No specific user input is required, so no fields are defined in this model.
    """

    pass


class Schedule(BaseModel):
    """
    Represents an event or task scheduled on a specific date, for specific activityType and resources, at a specific Field location.
    """

    id: int
    date: datetime
    activityType: prisma.enums.ActivityType
    staffDetailsId: int
    fieldId: Optional[int] = None


class InventoryItemDetailed(BaseModel):
    """
    Extended inventory item details including scheduling information for supply needs.
    """

    id: int
    name: str
    quantity: int
    status: prisma.enums.InventoryStatus
    type: prisma.enums.InventoryType
    next_replenishment_schedule: List[Schedule]


class GetSupplyChainItemsResponse(BaseModel):
    """
    Outputs detailed information about each item in the supply chain, including current stock levels, source details, and anticipated reordering needs based on schedules.
    """

    items: List[InventoryItemDetailed]


async def getSupplyChainItems(
    request: GetSupplyChainItemsRequest,
) -> GetSupplyChainItemsResponse:
    """
    Retrieves all items in the supply chain, including current stock levels, source details, and tracking information. This endpoint helps to monitor the overall supply chain flow and is essential for replenishment planning. It utilizes data from the Inventory Management module to accurately reflect stock levels and integrates with the Scheduling module to anticipate upcoming supply needs.

    Args:
        request (GetSupplyChainItemsRequest): Request model for fetching all inventory items in the supply chain. No specific user input is required, so no fields are defined in this model.

    Returns:
        GetSupplyChainItemsResponse: Outputs detailed information about each item in the supply chain, including current stock levels, source details, and anticipated reordering needs based on schedules.
    """
    inventory_items = await prisma.models.InventoryItem.prisma().find_many()
    detailed_items = []
    for item in inventory_items:
        schedules = await prisma.models.Schedule.prisma().find_many(
            where={
                "staffDetails": {
                    "schedules": {
                        "some": {
                            "date": {"gt": datetime.now()},
                            "activityType": {
                                "in": [
                                    prisma.enums.ActivityType.Planting,
                                    prisma.enums.ActivityType.Harvesting,
                                ]
                            },
                        }
                    }
                }
            }
        )
        detailed_item = InventoryItemDetailed(
            id=item.id,
            name=item.name,
            quantity=item.quantity,
            status=item.status,
            type=item.type,
            next_replenishment_schedule=schedules,
        )
        detailed_items.append(detailed_item)
    response = GetSupplyChainItemsResponse(items=detailed_items)
    return response
