import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteSalesResponse(BaseModel):
    """
    Response model confirming the deletion of a sales record. It contains a success message.
    """

    message: str


async def deleteSalesRecord(salesId: int) -> DeleteSalesResponse:
    """
    Deletes a specific sales record identified by the sales ID. This removal also adjusts the inventory and financial data within QuickBooks to reflect the change. Expected response is a success message confirming the deletion of the record.

    Args:
    salesId (int): The unique identifier for the sales record to be deleted.

    Returns:
    DeleteSalesResponse: Response model confirming the deletion of a sales record. It contains a success message.

    Example:
        salesId = 101
        response = await deleteSalesRecord(salesId)
        > DeleteSalesResponse(message='Sales record with ID 101 deleted successfully.')
    """
    transaction = await prisma.models.Transaction.prisma().find_unique(
        where={"id": salesId, "type": prisma.enums.TransactionType.Sale}
    )
    if not transaction:
        return DeleteSalesResponse(message=f"Sales record with ID {salesId} not found.")
    await prisma.models.Transaction.prisma().delete(where={"id": salesId})
    return DeleteSalesResponse(
        message=f"Sales record with ID {salesId} deleted successfully."
    )
