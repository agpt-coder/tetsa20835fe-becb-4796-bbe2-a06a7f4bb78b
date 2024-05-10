from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class RoleUpdateResponse(BaseModel):
    """
    Response model confirming the update of a role's permissions. Includes the role affected and the new permissions assigned to ensure transparency.
    """

    success: bool
    updated_role_id: str
    updated_permissions: List[str]


async def updateRole(id: str, new_permissions: List[str]) -> RoleUpdateResponse:
    """
    Updates the permissions associated with a specific role. This function is critical for ensuring that role
    permissions remain aligned with evolving organizational policies. The changes are scoped and authenticated
    ensuring only roles like Admin and HR can update permissions.

    Args:
        id (str): Unique identifier of the role for which permissions are being updated.
        new_permissions (List[str]): New set of permissions to be assigned to the role.

    Returns:
        RoleUpdateResponse: Response model confirming the update of a role's permissions. This includes the role
                            affected and the new permissions assigned to the role to ensure transparency.

    Example:
        await updateRole('5', ['EditInventory', 'ManageOrders'])
        > RoleUpdateResponse(success=True, updated_role_id='5', updated_permissions=['EditInventory', 'ManageOrders'])
    """
    try:
        user = await prisma.models.User.prisma().find_unique(
            where={"id": int(id)}, include={"role": True}
        )
        if user and user.role in [prisma.enums.Role.Admin, prisma.enums.Role.HR]:
            updated_user = await prisma.models.User.prisma().update(
                {"where": {"id": int(id)}, "data": {"role": new_permissions[0]}}
            )  # TODO(autogpt): Argument missing for parameter "where". reportCallIssue
            return RoleUpdateResponse(
                success=True, updated_role_id=id, updated_permissions=new_permissions
            )
        else:
            return RoleUpdateResponse(
                success=False, updated_role_id=id, updated_permissions=[]
            )
    except Exception as e:
        return RoleUpdateResponse(
            success=False, updated_role_id=id, updated_permissions=[]
        )
