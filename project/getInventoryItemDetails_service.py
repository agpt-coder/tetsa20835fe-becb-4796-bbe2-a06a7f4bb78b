from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class InventoryItemResponse(BaseModel):
    """
    Detailed information about a specific inventory item, including its quantity, status, and type.
    """

    id: int
    name: str
    quantity: int
    status: prisma.enums.InventoryStatus
    type: prisma.enums.InventoryType
    lastUpdated: datetime


async def getInventoryItemDetails(itemId: int) -> InventoryItemResponse:
    """
    Fetches detailed information about a specific inventory item by item ID. Provides comprehensive details including quantity, status, last updated, and category. Useful for audits and detailed checks.

    Args:
        itemId (int): The unique identifier for the inventory item.

    Returns:
        InventoryItemResponse: Detailed information about a specific inventory item, including its quantity, status, and type.

    Example:
        inventory_item_details = await getInventoryItemDetails(1)
        print(inventory_item_details)
        > InventoryItemResponse(id=1, name='Sapling', quantity=100, status=prisma.enums.InventoryStatus.InStock, type=prisma.enums.InventoryType.Sapling, lastUpdated=datetime.datetime(2023, 12, 5, 10, 15))
    """
    inventory_item = await prisma.models.InventoryItem.prisma().find_unique(
        where={"id": itemId}
    )
    if inventory_item is None:
        raise ValueError("No inventory item found with the given ID.")
    return InventoryItemResponse(
        id=inventory_item.id,
        name=inventory_item.name,
        quantity=inventory_item.quantity,
        status=inventory_item.status,
        type=inventory_item.type,
        lastUpdated=inventory_item.transactions[-1].date
        if inventory_item.transactions
        else None,
    )
