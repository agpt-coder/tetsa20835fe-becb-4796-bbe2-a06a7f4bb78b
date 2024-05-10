from enum import Enum
from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateFarmLayoutResponse(BaseModel):
    """
    Response after attempting to update a farm layout's details. Includes success status and the updated properties if applicable.
    """

    layoutId: int
    updatedFields: Dict[str, Any]
    success: bool


class FieldCondition(Enum):
    Healthy: str = "Healthy"
    NeedsAttention: str = "NeedsAttention"
    Critical: str = "Critical"


async def updateFarmLayout(
    layoutId: int,
    name: Optional[str] = None,
    areaSize: Optional[float] = None,
    mapUrl: Optional[str] = None,
    condition: Optional[FieldCondition] = None,
) -> UpdateFarmLayoutResponse:
    """
    Updates an existing farm layout. It requires layoutId as a path parameter and updates fields based on the submitted data. Changes might include reassignment of areas or updates in layout dimensions, maintained through GIS standards.

    Args:
        layoutId (int): The unique identifier for the farm layout to be updated.
        name (Optional[str]): New name for the designated area, if it needs to be updated.
        areaSize (Optional[float]): New size of the area in appropriate units (e.g., acres).
        mapUrl (Optional[str]): Updated URL linking to the new GIS layout map, if available.
        condition (Optional[FieldCondition]): Updated condition of this field, from a predefined set of FieldCondition values.

    Returns:
        UpdateFarmLayoutResponse: Response after attempting to update a farm layout's details. Includes success status and the updated properties if applicable.
    """
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if areaSize is not None:
        update_data["areaSize"] = areaSize
    if mapUrl is not None:
        update_data["mapUrl"] = mapUrl
    if condition is not None:
        update_data["condition"] = condition
    try:
        updated_field = await prisma.models.Field.prisma().update(
            where={"id": layoutId}, data=update_data
        )  # TODO(autogpt): "Field" is not exported from module "prisma.models". reportPrivateImportUsage
        updated_fields = {
            key: getattr(updated_field, key, None) for key in update_data.keys()
        }
        return UpdateFarmLayoutResponse(
            layoutId=layoutId, updatedFields=updated_fields, success=True
        )
    except Exception as e:
        return UpdateFarmLayoutResponse(
            layoutId=layoutId, updatedFields={}, success=False
        )
