from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class TransactionDetails(BaseModel):
    """
    Includes details like transaction type, date, and additional notes.
    """

    transaction_type: prisma.enums.TransactionType
    transaction_date: datetime
    notes: Optional[str] = None


class SalesRecordResponse(BaseModel):
    """
    Confirmation response upon successful addition of a new sales record, including the reference ID.
    """

    success: bool
    record_id: int
    message: Optional[str] = None


async def createSalesRecord(
    items_sold: List[int],
    customer_id: int,
    total_amount: float,
    transaction_details: TransactionDetails,
) -> SalesRecordResponse:
    """
    Adds a new sales record to the system. This endpoint accepts sales data, including details of the items sold, customer information, and transaction amount. It updates the system and QuickBooks post validation of the data received from Order Management. Expected response confirms successful creation with a reference to the new sales record ID.

    Args:
        items_sold (List[int]): List of item IDs sold in the transaction.
        customer_id (int): The ID of the customer making the purchase.
        total_amount (float): Total transaction amount for the sales.
        transaction_details (TransactionDetails): Details of the payment transaction.

    Returns:
        SalesRecordResponse: Confirmation response upon successful addition of a new sales record, including the reference ID.
    """
    try:
        transaction = await prisma.models.Transaction.prisma().create(
            data={
                "type": transaction_details.transaction_type.value,
                "date": transaction_details.transaction_date,
                "amount": total_amount,
                "userId": customer_id,
                "inventoryItemId": items_sold,
                "notes": transaction_details.notes,
            }
        )
        return SalesRecordResponse(
            success=True,
            record_id=transaction.id,
            message="Sales record created successfully.",
        )
    except Exception as e:
        return SalesRecordResponse(
            success=False,
            record_id=0,
            message=f"An error occurred while creating the sales record: {str(e)}",
        )
