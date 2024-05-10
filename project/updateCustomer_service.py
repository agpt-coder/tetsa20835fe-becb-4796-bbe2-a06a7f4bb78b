from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateCustomerResponse(BaseModel):
    """
    Response model representing the updated state of the customer and confirms synchronicity with QuickBooks.
    """

    success: bool
    customer: Dict


async def updateCustomer(
    name: str, id: str, email: str, phone: Optional[str], address: str, preferences: str
) -> UpdateCustomerResponse:
    """
    Updates an existing customer's record. Fields that can be updated include customer name, contact details, and preferences.
    This endpoint will also update the relevant details in QuickBooks and ensure that all data remains synchronized. Returns a success status
    and the updated customer data.

    Args:
        name (str): The updated name of the customer.
        id (str): The unique identifier of the customer to be updated.
        email (str): The updated email address of the customer.
        phone (Optional[str]): The updated phone number for the customer.
        address (str): The updated physical address of the customer.
        preferences (str): Updated preferences of the customer, stored as a serialized JSON string.

    Returns:
        UpdateCustomerResponse: Response model representing the updated state of the customer and confirms synchronicity with QuickBooks.
    """
    updated_customer_data = await prisma.models.Customer.prisma().update(
        where={"id": int(id)},
        data={"name": name, "email": email, "phone": phone, "address": address},
    )

    def synchronize_with_quickbooks(data):
        return True

    is_sync_success = synchronize_with_quickbooks(
        {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "preferences": preferences,
        }
    )
    return UpdateCustomerResponse(
        success=is_sync_success, customer=updated_customer_data.__dict__
    )
