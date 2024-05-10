from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetRolesRequest(BaseModel):
    """
    Retrieves all available roles and their associated permissions. Requires admin or HR level access.
    """

    pass


class RolePermissions(BaseModel):
    """
    This object includes the role description along with the detailed permissions.
    """

    role: prisma.enums.Role
    permissions: List[str]


class GetRolesResponse(BaseModel):
    """
    Provides a list of all roles within the organization along with their designated permissions.
    """

    roles: List[RolePermissions]


async def listRoles(request: GetRolesRequest) -> GetRolesResponse:
    """
    Provides a list of all staff roles and associated permissions, aiding in access control and role assignments.
    Accessible by Admin and HR for management and oversight.

    Args:
        request (GetRolesRequest): Object to retrieve all available roles and their associated permissions.
                                   Requires admin or HR level access.

    Returns:
        GetRolesResponse: Object containing a list of all roles within the organization along with their designated permissions.
    """
    users = await prisma.models.User.prisma().find_many(include={"role": True})
    role_permissions_mapping = {}
    for user in users:
        if user.role not in role_permissions_mapping:
            role_permissions_mapping[user.role] = set()
        role_permissions_mapping[user.role].update(["edit_profile", "view_reports"])
    roles_info = [
        RolePermissions(role=role, permissions=list(permissions))
        for role, permissions in role_permissions_mapping.items()
    ]
    response = GetRolesResponse(roles=roles_info)
    return response
