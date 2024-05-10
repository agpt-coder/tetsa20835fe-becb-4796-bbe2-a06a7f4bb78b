from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateSupplyChainItemResponse(BaseModel):
    """
    This model outlines the result of the update operation on a supply chain item and includes the new state of the item.
    """

    success: bool
    updatedItem: prisma.models.InventoryItem
    message: str


async def updateSupplyChainItem(
    itemId: int, quantity: int, supplierName: str, expectedDelivery: datetime
) -> UpdateSupplyChainItemResponse:
    """
    Updates the details of an existing supply chain item. This can include changes to quantity, supplier information, and expected delivery dates. It is crucial for maintaining accurate and up-to-date information on the supplies necessary for farm operations. Changes here are reflected in the Inventory Management system for seamless stock updates.

    Args:
        itemId (int): The unique identifier of the inventory item being updated.
        quantity (int): The new quantity of the item in the inventory.
        supplierName (str): The name of the supplier for this item.
        expectedDelivery (datetime): The expected delivery date of the item from the supplier.

    Returns:
        UpdateSupplyChainItemResponse: This model outlines the result of the update operation on a supply chain item and includes the new state of the item.
    """
    try:
        inventory_item = await prisma.models.InventoryItem.prisma().find_unique(
            where={"id": itemId}, include={"transactions": True}
        )
        if inventory_item is None:
            return UpdateSupplyChainItemResponse(
                success=False,
                updatedItem=None,
                message="No item found with the given ID.",
            )
        updated_inventory_item = await prisma.models.InventoryItem.prisma().update(
            where={"id": itemId},
            data={
                "quantity": quantity,
                "name": supplierName,
                "status": "InStock" if quantity > 0 else "OutOfStock",
            },
        )
        return UpdateSupplyChainItemResponse(
            success=True,
            updatedItem=updated_inventory_item,
            message="Item successfully updated.",
        )
    except Exception as e:
        return UpdateSupplyChainItemResponse(
            success=False, updatedItem=None, message=f"Error updating item: {str(e)}"
        )
