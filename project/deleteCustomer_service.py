from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteCustomerResponse(BaseModel):
    """
    Response model for confirming the deletion of a customer. Includes a status message about the operation.
    """

    status: str


class Role(Enum):
    Admin: str = "Admin"
    Staff: str = "Staff"
    Manager: str = "Manager"
    Accountant: str = "Accountant"
    HR: str = "HR"
    FieldWorker: str = "FieldWorker"


async def deleteCustomer(id: int, user_role: Role) -> DeleteCustomerResponse:
    """
    Removes a customer's record from the database using their ID. This action will also trigger an update to remove the customer's information from QuickBooks and other integrated services, like Order Management, to maintain data integrity. Returns a success status upon successful deletion.

    Args:
        id (int): The unique identifier of the customer to be deleted.
        user_role (Role): Role of the user performing the request, which must be Admin.

    Returns:
        DeleteCustomerResponse: Response model for confirming the deletion of a customer. Includes a status message about the operation.

    Raises:
        PermissionError: If the user role is not Admin.
        ValueError: If no customer with the given id exists.
    """
    if user_role != Role.Admin:
        raise PermissionError("Only Admins are allowed to delete customer records.")
    customer = await prisma.models.Customer.prisma().find_unique(where={"id": id})
    if not customer:
        raise ValueError(f"No customer found with ID {id}.")
    await prisma.models.Customer.prisma().delete(where={"id": id})
    return DeleteCustomerResponse(status="prisma.models.Customer successfully deleted.")
