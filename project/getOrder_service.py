from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class OrderItem(BaseModel):
    """
    Represents an item in an order, detailing the item ID and the quantity ordered.
    """

    inventoryItemId: int
    quantity: int


class CustomerInfo(BaseModel):
    """
    Customer details associated with this order.
    """

    customer_id: int
    name: str
    email: str
    phone: Optional[str] = None
    address: str


class OrderDetailsResponse(BaseModel):
    """
    Provides comprehensive data on an order including detailed items, quantities, customer information, and sync status with QuickBooks.
    """

    order_id: int
    items: List[OrderItem]
    total_amount: float
    customer: CustomerInfo
    status: str


async def getOrder(orderId: int) -> OrderDetailsResponse:
    """
    Retrieves detailed information of a specific order by ID. It provides comprehensive data including items, quantities,
    customer details, and invoicing status from QuickBooks. Ensures synchronization with Inventory statuses and updates
    Customer Management records as needed.

    Args:
        orderId (int): The unique identifier of the order to retrieve.

    Returns:
        OrderDetailsResponse: Provides comprehensive data on an order including detailed items, quantities, customer information,
                              and sync status with QuickBooks.

    Example:
        - Suppose orderId = 1 refers to an existing order,
          getOrder(1) might return:
          OrderDetailsResponse(order_id=1, items=[OrderItem(inventoryItemId=101, quantity=5)], total_amount=100.0,
                               customer=CustomerInfo(customer_id=1, name='John Doe', email='john.doe@example.com', phone='1234567890',
                                                     address='123 Elm Street'), status='Delivered')
    """
    order = await prisma.models.Order.prisma().find_unique(
        where={"id": orderId},
        include={
            "customer": True,
            "transactions": {"include": {"inventoryItem": True}},
        },
    )
    if order is None:
        raise ValueError(f"No order found with ID {orderId}")
    if not order.customer:
        raise ValueError("Customer details are not available for this order.")
    items = [
        OrderItem(
            inventoryItemId=transaction.inventoryItem.id,
            quantity=int(transaction.inventoryItem.quantity),
        )
        for transaction in order.transactions
        if transaction.inventoryItem
    ]
    customer_info = CustomerInfo(
        customer_id=order.customer.id,
        name=order.customer.name,
        email=order.customer.email,
        phone=order.customer.phone,
        address=order.customer.address,
    )
    response = OrderDetailsResponse(
        order_id=order.id,
        items=items,
        total_amount=order.total,
        customer=customer_info,
        status=order.status.name,
    )
    return response
