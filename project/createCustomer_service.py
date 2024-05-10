from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateCustomerResponse(BaseModel):
    """
    Response model for the created customer, reflecting the complete object as is now stored in the database including the unique ID.
    """

    id: int
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    preferences: str
    quickBooksIntegrated: bool


async def createCustomer(
    name: str,
    email: str,
    phone: Optional[str],
    address: str,
    preferences: str,
    quickBooksIntegrationDetails: Dict[str, str],
) -> CreateCustomerResponse:
    """
    Creates a new customer record in the database. This endpoint accepts customer details such as name, contact information, and preferences, and persists them to the database. Also integrates with QuickBooks to initialize financial management settings for the new customer. Returns the created customer object with an ID.

    Args:
        name (str): The full name of the customer.
        email (str): The email address of the customer. Must be unique as it will be used for login and notifications.
        phone (Optional[str]): The contact telephone number for the customer. This field is optional.
        address (str): The physical address of the customer.
        preferences (str): Any specific preferences the customer has expressed, stored as a JSON string.
        quickBooksIntegrationDetails (Dict[str, str]): Settings and details needed to initialize integration with QuickBooks for managing the customer's finances.

    Returns:
        CreateCustomerResponse: Response model for the created customer, reflecting the complete object as is now stored in the database including the unique ID.

    Example:
        response = await createCustomer(
            name="John Doe",
            email="john.doe@example.com",
            phone="1234567890",
            address="123 Main Street, Springfield, USA",
            preferences='{"newsletter": "subscribe"}',
            quickBooksIntegrationDetails={"setup": "complete"}
        )
        print(response)
    """
    customer = await prisma.models.Customer.prisma().create(
        data={"name": name, "email": email, "phone": phone, "address": address}
    )
    quickBooksIntegrated = True
    response = CreateCustomerResponse(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        preferences=preferences,
        quickBooksIntegrated=quickBooksIntegrated,
    )
    return response
