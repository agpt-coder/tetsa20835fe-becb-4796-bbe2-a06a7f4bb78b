from datetime import datetime
from typing import Dict, List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetSuppliersRequest(BaseModel):
    """
    This request model fetches details about all suppliers associated with the farm's supply chain.
    """

    pass


class InventoryDetail(BaseModel):
    """
    Detail of inventory item involved in the transaction.
    """

    itemName: str
    quantity: int


class TransactionDetail(BaseModel):
    """
    Details of each transaction made with the supplier.
    """

    date: datetime
    amount: float
    items: List[InventoryDetail]


class SupplierDetail(BaseModel):
    """
    Detailed information about a supplier including contact, supplied goods, and transaction history.
    """

    name: str
    contactInfo: Dict[str, str]
    goodsSupplied: List[str]
    historicalOrders: List[TransactionDetail]


class GetSuppliersResponse(BaseModel):
    """
    Provides a comprehensive list of suppliers, including their contact details, supplied goods type, and historical order data.
    """

    suppliers: List[SupplierDetail]


async def getSuppliers(request: GetSuppliersRequest) -> GetSuppliersResponse:
    """
    Lists all suppliers associated with the farm's supply chain. Provides contact information, type of goods supplied, and historical ordering data. This endpoint is vital for managing relationships with suppliers and planning future purchases. It assists in making informed decisions based on past performance and reliability.

    Args:
        request (GetSuppliersRequest): This request model fetches details about all suppliers associated with the farm's supply chain.

    Returns:
        GetSuppliersResponse: Provides a comprehensive list of suppliers, including their contact details, supplied goods type, and historical order data.
    """
    users = await prisma.models.User.prisma().find_many(
        where={"transactions": {"some": {}}},
        include={"transactions": True, "profile": True},
    )
    suppliers = []
    for user in users:
        if user.transactions:
            historical_orders = []
            goods_supplied = set()
            for transaction in user.transactions:
                if (
                    transaction.inventoryItem
                    and transaction.type == prisma.enums.TransactionType.Purchase
                ):
                    inventory_details = (
                        await prisma.models.InventoryItem.prisma().find_unique(
                            where={"id": transaction.inventoryItemId}
                        )
                    )
                    if inventory_details:
                        goods_supplied.add(inventory_details.name)
                        transaction_details = TransactionDetail(
                            date=transaction.date,
                            amount=transaction.amount,
                            items=[
                                InventoryDetail(
                                    itemName=inventory_details.name,
                                    quantity=inventory_details.quantity,
                                )
                            ],
                        )
                        historical_orders.append(transaction_details)
            if user.profile:
                supplier_info = SupplierDetail(
                    name=f"{user.profile.firstName} {user.profile.lastName}",
                    contactInfo={
                        "email": user.email,
                        "phone": user.profile.phone if user.profile.phone else "N/A",
                    },
                    goodsSupplied=list(goods_supplied),
                    historicalOrders=historical_orders,
                )
                suppliers.append(supplier_info)
    response = GetSuppliersResponse(suppliers=suppliers)
    return response
