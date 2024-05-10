from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class FetchSalesDataRequest(BaseModel):
    """
    Request model for fetching sales data does not require specific input fields as it fetches all records. Future enhancements might include parameters for filtering by date or amount range.
    """

    pass


class Customer(BaseModel):
    """
    Details of the customer associated with the transaction.
    """

    name: str
    email: str
    phone: Optional[str] = None


class ProductDetails(BaseModel):
    """
    Product-specific details.
    """

    product_id: int
    product_name: str
    product_type: str


class SaleRecord(BaseModel):
    """
    Detailed information about each sale.
    """

    transaction_id: int
    transaction_date: datetime
    transaction_amount: float
    customer_details: Customer
    product_details: ProductDetails


class SalesRecordListResponse(BaseModel):
    """
    Response model for sales records, each record includes details like transaction ID, date, amount, and associated customer and product details, formatted for integration with QuickBooks.
    """

    sales_records: List[SaleRecord]


async def getSalesData(request: FetchSalesDataRequest) -> SalesRecordListResponse:
    """
    Retrieves a list of all sales records. This endpoint fetches detailed sales information, analyzes trends,
    and prepares data for financial reporting. The data is fetched in coordination with updates received from
    the Order Management module and is formatted for QuickBooks integration.

    Args:
        request (FetchSalesDataRequest): Request model for fetching sales data which does not require
                                         specific input fields as it fetches all records.

    Returns:
        SalesRecordListResponse: Response model for sales records, each record includes details like transaction ID,
                                 date, amount, and associated customer and product details,
                                 formatted for integration with QuickBooks.
    """
    transactions = await prisma.models.Transaction.prisma().find_many(
        where={"type": prisma.enums.TransactionType.Sale},
        include={"user": True, "inventoryItem": True},
    )
    sales_records = []
    for transaction in transactions:
        if (
            transaction.user is not None
            and transaction.user.profile is not None
            and (transaction.inventoryItem is not None)
        ):
            product_details = ProductDetails(
                product_id=transaction.inventoryItem.id,
                product_name=transaction.inventoryItem.name,
                product_type=transaction.inventoryItem.type,
            )
            customer_details = Customer(
                name=transaction.user.profile.firstName
                + " "
                + transaction.user.profile.lastName,
                email=transaction.user.email,
                phone=transaction.user.profile.phone,
            )
            sale_record = SaleRecord(
                transaction_id=transaction.id,
                transaction_date=transaction.date,
                transaction_amount=transaction.amount,
                customer_details=customer_details,
                product_details=product_details,
            )
            sales_records.append(sale_record)
    response = SalesRecordListResponse(sales_records=sales_records)
    return response
