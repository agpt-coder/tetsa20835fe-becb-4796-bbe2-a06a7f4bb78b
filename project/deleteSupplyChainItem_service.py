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


class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int
    status: str
    type: str


async def deleteSupplyChainItem(itemId: int) -> DeleteInventoryItemResponse:
    """
    Removes an item from the supply chain. This endpoint is used when an item is
    no longer needed or if the order was cancelled. It ensures the Supply Chain Management
    system remains clean and up-to-date, also reflecting changes in the Inventory Management
    system to keep stock levels accurate.

    Args:
        itemId (int): The unique identifier for the inventory item to be deleted.

    Returns:
        DeleteInventoryItemResponse: Response model that provides confirmation of deletion
        and details of the updated inventory list.
    """
    item_to_delete = await prisma.models.InventoryItem.prisma().delete(
        where={"id": itemId}
    )
    remaining_items = await prisma.models.InventoryItem.prisma().find_many()
    if item_to_delete is None:
        return DeleteInventoryItemResponse(
            success=False, remainingItems=remaining_items
        )
    return DeleteInventoryItemResponse(
        success=True,
        remainingItems=[
            prisma.models.InventoryItem.from_orm(i) for i in remaining_items
        ],
    )
