import prisma
import prisma.models
from pydantic import BaseModel


class DeleteStaffResponse(BaseModel):
    """
    A simple response model indicating the success of the deletion operation. It includes the status of the request and a message for clarity.
    """

    success: bool
    message: str


async def deleteStaff(id: int) -> DeleteStaffResponse:
    """
    Deletes a staff member's record from the system. Restricted solely to Admin and HR to ensure security and control over staffing changes.

    Args:
    id (int): The unique identifier of the staff member to be deleted. Only users with specified roles are allowed to perform this action.

    Returns:
    DeleteStaffResponse: A simple response model indicating the success of the deletion operation. It includes the status of the request and a message for clarity.

    Example:
      # Assuming the id of the staff member is 1 and they exist within the system:
      response = await deleteStaff(1)
      print(response.success, response.message)
      > True, "Staff member successfully deleted."
    """
    staff_member = await prisma.models.StaffDetails.prisma().find_first(
        where={"userId": id}
    )
    if staff_member is None:
        return DeleteStaffResponse(
            success=False, message=f"Staff member with ID {id} not found."
        )
    result = await prisma.models.User.prisma().delete(where={"id": staff_member.userId})
    if result:
        return DeleteStaffResponse(
            success=True, message="Staff member successfully deleted."
        )
    return DeleteStaffResponse(
        success=False, message=f"Failed to delete staff member with ID {id}."
    )
