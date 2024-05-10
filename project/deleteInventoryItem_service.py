from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteInventoryItemResponse(BaseModel):
    """
    Response model that provides confirmation of deletion and details of the updated inventory list.
    """

    success: bool
    remainingItems: List[prisma.models.InventoryItem]


async def deleteInventoryItem(itemId: int) -> DeleteInventoryItemResponse:
    """
    Deletes an item from inventory when it is no longer available or needed. This endpoint needs the item ID. A successful deletion will be confirmed along with an updated list of remaining inventory items.

    Args:
    itemId (int): The unique identifier for the inventory item to be deleted.

    Returns:
    DeleteInventoryItemResponse: Response model that provides confirmation of deletion and details of the updated inventory list.
    """
    inventory_item = await prisma.models.InventoryItem.prisma().delete(
        where={"id": itemId}
    )
    if inventory_item:
        remaining_items = await prisma.models.InventoryItem.prisma().find_many()
        return DeleteInventoryItemResponse(success=True, remainingItems=remaining_items)
    else:
        return DeleteInventoryItemResponse(success=False, remainingItems=[])
