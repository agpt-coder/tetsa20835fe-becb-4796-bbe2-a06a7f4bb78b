from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class InventoryItemDetails(BaseModel):
    """
    Detailed breakdown of inventory item properties.
    """

    name: str
    quantity: int
    status: str
    type: str


class InventoryListResponse(BaseModel):
    """
    Response format for the list of inventory items, showing name, quantity, and status for each.
    """

    item: List[InventoryItemDetails]


async def getInventory(
    type: Optional[str] = None, status: Optional[str] = None
) -> InventoryListResponse:
    """
    Retrieves the current stock levels of all inventory items including trees, fertilizers, and other related items. This function uses queries to filter data based on item type, status, and other parameters. Expected to respond with a list of items, their quantities, and statuses.

    Args:
        type (Optional[str]): Filter inventory items by type. This refers to whether the item is a tree, fertilizer, etc.
        status (Optional[str]): Filter inventory items by their stock status, such as 'InStock', 'LowStock', or 'OutOfStock'.

    Returns:
        InventoryListResponse: Response format for the list of inventory items, showing name, quantity, and status for each.

    Example:
        getInventory(type='Tree', status='LowStock')
        > InventoryListResponse(items=[
            InventoryItemDetails(name='Pine Tree', quantity=20, status='LowStock', type='Tree'),
            InventoryItemDetails(name='Spruce', quantity=15, status='LowStock', type='Tree')
          ])
    """
    filters = {}
    if type:
        filters["type"] = {"equals": type}
    if status:
        filters["status"] = {"equals": status}
    items = await prisma.models.InventoryItem.prisma().find_many(where=filters)
    details = [
        InventoryItemDetails(
            name=item.name, quantity=item.quantity, status=item.status, type=item.type
        )
        for item in items
    ]
    return InventoryListResponse(item=details)
