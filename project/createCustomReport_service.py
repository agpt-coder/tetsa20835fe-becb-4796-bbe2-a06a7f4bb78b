from datetime import date, datetime
from typing import List, Mapping

import prisma
import prisma.models
from pydantic import BaseModel


class CustomReportResponse(BaseModel):
    """
    Model for the response data of a custom report. It holds the generated report data.
    """

    report_id: str
    created_at: datetime
    report_data: str
    status: str


async def createCustomReport(
    report_type: str,
    date_range: Mapping[str, date],
    data_sources: List[str],
    group_by: List[str],
    order_by: List[str],
    aggregate_functions: Mapping[str, str],
    format: str,
) -> CustomReportResponse:
    """
    Allows users to generate custom reports based on specified parameters and data sources.
    Users can define what data to aggregate and the format of reporting. Expect a JSON representation
    of the created report. This endpoint facilitates specialized reporting for unique business insights.

    Args:
        report_type (str): Type of the report to generate, e.g., 'financial', 'operational'.
        date_range (Mapping[str, date]): The range of dates for which the report is to be generated.
        data_sources (List[str]): List of data sources to include in the report, e.g., 'Sales', 'Inventory', 'Payroll'.
        group_by (List[str]): Fields to group the data by in the report.
        order_by (List[str]): Fields to order the data by in the report.
        aggregate_functions (Mapping[str, str]): Aggregate functions to apply on data fields, e.g., 'sum', 'average'.
        format (str): The output format of the report, e.g., 'JSON', 'CSV'.

    Returns:
        CustomReportResponse: Model for the response data of a custom report. It holds the generated report data.
    """
    start_date = date_range["start"]
    end_date = date_range["end"]
    transactions = await prisma.models.Transaction.prisma().find_many(
        where={
            "date": {"gte": start_date, "lte": end_date},
            "type": {"in": data_sources},
        }
    )
    report_content = f"Report from {start_date} to {end_date}, including {len(transactions)} transactions."
    created_report = await prisma.models.Report.prisma().create(
        data={
            "title": f"{report_type.capitalize()} report",
            "content": report_content,
            "date": datetime.now(),
        }
    )
    return CustomReportResponse(
        report_id=str(created_report.id),
        created_at=created_report.date,
        report_data=created_report.content,
        status="completed",
    )
