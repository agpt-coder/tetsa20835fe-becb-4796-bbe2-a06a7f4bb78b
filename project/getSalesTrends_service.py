from datetime import date
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetSalesTrendsResponse(BaseModel):
    """
    The output model for sales trends analysis, which may include graphs or structured data for integration with business reports.
    """

    trend_data: str
    graphical_data: Optional[str] = None


async def getSalesTrends(
    start_date: date, end_date: date, group_by: str
) -> GetSalesTrendsResponse:
    """
    Analyzes and retrieves sales trends over a specified period. This function fetches transaction data from the database,
    grouped according to the specified criteria ('monthly', 'product', or 'category') to aid in financial decision-making
    and report generation, especially integrating with systems like QuickBooks.

    Args:
        start_date (date): The start date for the period over which sales data should be analyzed.
        end_date (date): The end date for the period over which sales data should be analyzed.
        group_by (str): The criteria for grouping sales data.

    Returns:
        GetSalesTrendsResponse: The output model for sales trends analysis, which may include graphs or structured data for integration with business reports.

    Example:
        from datetime import date
        response = await getSalesTrends(date(2023, 1, 1), date(2023, 3, 31), 'monthly')
        print(response.trend_data)
    """
    transactions = await prisma.models.Transaction.prisma().find_many(
        where={
            "type": prisma.enums.TransactionType.SALE,
            "date": {"gte": start_date, "lte": end_date},
        }
    )  # TODO(autogpt): Cannot access member "SALE" for type "type[TransactionType]"
    #     Member "SALE" is unknown. reportAttributeAccessIssue
    trend_data = {}
    for transaction in transactions:
        if group_by == "monthly":
            key = transaction.date.strftime("%Y-%m")
        elif group_by == "product" and transaction.inventoryItem:
            key = transaction.inventoryItem.name
        elif group_by == "category" and transaction.inventoryItem:
            key = transaction.inventoryItem.type.name
        else:
            continue
        if key not in trend_data:
            trend_data[key] = {
                "total_sales": 0,
                "transaction_count": 0,
                "average_sale": 0,
            }
        trend_data[key]["total_sales"] += transaction.amount
        trend_data[key]["transaction_count"] += 1
    for key, values in trend_data.items():
        if values["transaction_count"] > 0:
            values["average_sale"] = values["total_sales"] / values["transaction_count"]
    trend_data_str = str(trend_data)
    return GetSalesTrendsResponse(trend_data=trend_data_str)
