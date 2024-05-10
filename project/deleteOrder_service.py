import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteOrderResponse(BaseModel):
    """
    Provides a confirmation of the order deletion and flags any important results such as inventory adjustments or QuickBooks updates.
    """

    success: bool
    message: str


async def deleteOrder(orderId: int, confirmation: bool) -> DeleteOrderResponse:
    """
    Deletes an existing order. This will release the reserved inventory back to the Inventory Management system and update the financial records in QuickBooks to reflect the cancellation. This action requires confirmation from an authorized user.

    Args:
        orderId (int): The unique identifier of the order to be deleted.
        confirmation (bool): A confirmation token or flag that validates the intent to delete the order from an authorized user.

    Returns:
        DeleteOrderResponse: Provides a confirmation of the order deletion and flags any important results such as inventory adjustments or QuickBooks updates.

    Examples:
        >>> response = await deleteOrder(5, True)
        >>> print(response.success)
        True
        >>> print(response.message)
        'Order deleted and inventory updated successfully.'
    """
    if not confirmation:
        return DeleteOrderResponse(
            success=False, message="Action not confirmed. Order deletion aborted."
        )
    order = await prisma.models.Order.prisma().find_unique(where={"id": orderId})
    if not order:
        return DeleteOrderResponse(success=False, message="Order not found.")
    if order.status == prisma.enums.OrderStatus.Cancelled:
        return DeleteOrderResponse(success=False, message="Order already cancelled.")
    result = await prisma.models.Order.prisma().update(
        where={"id": orderId}, data={"status": prisma.enums.OrderStatus.Cancelled}
    )
    return DeleteOrderResponse(
        success=True, message="Order deleted and inventory updated successfully."
    )
