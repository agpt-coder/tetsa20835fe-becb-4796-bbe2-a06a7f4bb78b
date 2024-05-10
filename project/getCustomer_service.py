from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Customer(BaseModel):
    """
    Details of the customer associated with the transaction.
    """

    name: str
    email: str
    phone: Optional[str] = None


class Order(BaseModel):
    """
    Pydantic model for handling order details in customer responses.
    """

    date: datetime
    total: float
    status: prisma.enums.OrderStatus


class Transaction(BaseModel):
    """
    Pydantic model for transaction details linked to the customer.
    """

    type: prisma.enums.TransactionType
    date: datetime
    amount: float


class GetCustomerDetailsResponse(BaseModel):
    """
    Response model containing detailed information about a customer, including transaction history and order details.
    """

    customer: Customer
    orders: List[Order]
    transactions: List[Transaction]


async def getCustomer(id: str) -> GetCustomerDetailsResponse:
    """
    Retrieves detailed information about a specific customer using their unique ID. This information includes name, contact details, preferences, and historical transaction data. It interacts with QuickBooks to fetch financial data related to the customer and with Order Management to retrieve order history. Expected to return a JSON object containing the customer's information.

    Args:
    id (str): The unique identifier of the customer.

    Returns:
    GetCustomerDetailsResponse: Response model containing detailed information about a customer, including transaction history and order details.
    """
    customer_record = await prisma.models.Customer.prisma().find_unique(
        where={"id": int(id)}, include={"orders": {"include": {"transactions": True}}}
    )
    if customer_record is None:
        raise ValueError(f"No customer found with ID {id}")
    customer_details = Customer(
        name=customer_record.name,
        email=customer_record.email,
        phone=customer_record.phone,
    )
    orders = [
        Order(date=o.date, total=o.total, status=prisma.enums.OrderStatus(o.status))
        for o in customer_record.orders or []
    ]
    transactions = [
        Transaction(
            type=prisma.enums.TransactionType(t.type), date=t.date, amount=t.amount
        )
        for o in customer_record.orders or []
        for t in o.transactions or []
    ]
    response = GetCustomerDetailsResponse(
        customer=customer_details, orders=orders, transactions=transactions
    )
    return response
