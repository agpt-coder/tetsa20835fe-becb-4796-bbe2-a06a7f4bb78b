import prisma
import prisma.models
from pydantic import BaseModel


class UpdateSupplierResponse(BaseModel):
    """
    Response model providing confirmation and updated details of the supplier
    """

    supplierId: int
    updated: bool


async def updateSupplier(
    supplierId: int,
    name: str,
    contactName: str,
    contactEmail: str,
    contactPhone: str,
    address: str,
) -> UpdateSupplierResponse:
    """
    Updates existing supplier information. This is crucial for keeping supplier details current, which is essential for ongoing supply chain management. Ensures communication and orders are directed correctly and helps maintain strong supplier relationships.

    Args:
        supplierId (int): The unique identifier for the supplier
        name (str): The supplier's updated name
        contactName (str): The contact person's name at the supplier's end
        contactEmail (str): Updated contact email for reaching the supplier
        contactPhone (str): Updated contact phone number for the supplier
        address (str): The updated physical address of the supplier

    Returns:
        UpdateSupplierResponse: Response model providing confirmation and updated details of the supplier
    """
    customer_record = await prisma.models.Customer.prisma().find_unique(
        where={"id": supplierId}
    )
    if customer_record is None:
        raise ValueError("Supplier with this id does not exist.")
    updated_customer = await prisma.models.Customer.prisma().update(
        where={"id": supplierId},
        data={
            "name": name,
            "phone": contactPhone,
            "email": contactEmail,
            "address": address,
        },
    )
    return UpdateSupplierResponse(
        supplierId=supplierId, updated=True if updated_customer else False
    )
