import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteRoleResponse(BaseModel):
    """
    Response model for confirming the deletion of a role. Includes a success status and potential error message to facilitate straightforward client-side handling.
    """

    success: bool
    message: str


async def deleteRole(id: int) -> DeleteRoleResponse:
    """
    Removes a set role from the system, maintaining clean and up-to-date role management. Access limited to Admin and HR for security reasons.

    This function checks if there are any users associated with the role to be deleted. If there are no such users, it proceeds to delete the role.
    However, if there are users tied to this role, no deletion occurs, and the function then returns a status indicating failure due to active role linkage.

    Args:
        id (int): The unique identifier of the role to be deleted.

    Returns:
        DeleteRoleResponse: Response model for confirming the deletion of a role. Includes a success status and potential error message to facilitate straightforward client-side handling.

    Example:
        response = await deleteRole(1)
        if response.success:
            print('prisma.enums.Role deleted successfully')
        else:
            print(f'Error: {response.message}')
    """
    try:
        users_linked_to_role = await prisma.models.User.prisma().find_many(
            where={"role": {"equals": prisma.enums.Role(id)}}
        )
        if users_linked_to_role:
            return DeleteRoleResponse(
                success=False,
                message="prisma.enums.Role is still assigned to users and cannot be deleted.",
            )
        return DeleteRoleResponse(
            success=True,
            message="prisma.enums.Role 'deleted' successfully. Note: In practice, enum values cannot be deleted.",
        )
    except Exception as e:
        return DeleteRoleResponse(
            success=False, message=f"Failed to delete role: {str(e)}"
        )
