from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetFarmLayoutRequest(BaseModel):
    """
    Request model for fetching all farm layouts. No specific parameters are used in this GET request.
    """

    pass


class FieldDetail(BaseModel):
    """
    Detailed information about each field, including its identifier, area size, condition, and GIS map URL.
    """

    fieldId: int
    fieldName: str
    areaSize: float
    condition: prisma.enums.FieldCondition
    mapUrl: str


class GetFarmLayoutResponse(BaseModel):
    """
    Response model for providing detailed information about farm layouts, including mapping and field conditions. Utilizes the 'Field' database model to outline detailed setups.
    """

    farmLayouts: List[FieldDetail]


async def getFarmLayouts(request: GetFarmLayoutRequest) -> GetFarmLayoutResponse:
    """
    Retrieves all farm layouts. Expected to return a detailed map of the farm layout including field identifiers and conditions. It will leverage GIS mapping functionalities to present a spatial view of the premises.

    Args:
        request (GetFarmLayoutRequest): Request model for fetching all farm layouts. No specific parameters are used in this GET request.

    Returns:
        GetFarmLayoutResponse: Response model for providing detailed information about farm layouts, including mapping and field conditions. Utilizes the 'prisma.models.Field' database model to outline detailed setups.
    """
    fields = (
        await prisma.models.Field.prisma().find_many()
    )  # TODO(autogpt): "Field" is not exported from module "prisma.models". reportPrivateImportUsage
    farm_layouts = [
        FieldDetail(
            fieldId=field.id,
            fieldName=field.name,
            areaSize=field.areaSize,
            condition=field.condition.name,
            mapUrl=field.mapUrl,
        )
        for field in fields
    ]
    return GetFarmLayoutResponse(farmLayouts=farm_layouts)
