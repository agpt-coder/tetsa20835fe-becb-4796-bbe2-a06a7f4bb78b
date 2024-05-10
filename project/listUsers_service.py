from typing import Any, Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetUsersResponse(BaseModel):
    """
    Contains the paginated user profiles and pagination metadata, structured to make client-side rendering easier and more efficient.
    """

    users: List[Dict[str, Any]]
    totalPages: int
    currentPage: int
    totalItems: int


async def listUsers(
    page: int, pageSize: int, role: Optional[str], email: Optional[str]
) -> GetUsersResponse:
    """
    Lists all user profiles with pagination support. Optionally filters by role or email if specified in the query. Primarily used by Admin and HR for oversight and management.

    Args:
        page (int): The page number in the pagination sequence.
        pageSize (int): The number of items to display per page.
        role (Optional[str]): Optional filter for user accounts by role to enable targeted fetching especially useful for large datasets.
        email (Optional[str]): Optional field to filter users by their email addresses.

    Returns:
        GetUsersResponse: Contains the paginated user profiles and pagination metadata, structured to make client-side rendering easier and more efficient.
    """
    where_clauses = {}
    if role:
        where_clauses["role"] = {"equals": role}
    if email:
        where_clauses["email"] = {"equals": email}
    total_users = await prisma.models.User.prisma().count(where=where_clauses)
    users = await prisma.models.User.prisma().find_many(
        where=where_clauses,
        skip=(page - 1) * pageSize,
        take=pageSize,
        include={"profile": True},
    )
    user_dicts = []
    for user in users:
        user_dicts.append(
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "profile": {
                    "firstName": user.profile.firstName,
                    "lastName": user.profile.lastName,
                    "phone": user.profile.phone,
                }
                if user.profile
                else {},
            }
        )
    totalPages = (total_users + pageSize - 1) // pageSize
    return GetUsersResponse(
        users=user_dicts,
        totalPages=totalPages,
        currentPage=page,
        totalItems=total_users,
    )
