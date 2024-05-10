from datetime import date, datetime
from typing import Dict, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class FinancialReportResponse(BaseModel):
    """
    Contains structured financial data including sale totals, expense totals, profitability metrics, and related breakdowns.
    """

    totalSales: float
    totalExpenses: float
    profitability: float
    salesBreakdown: Dict[str, float]
    expenseBreakdown: Dict[str, float]


async def getFinancialReports(
    startDate: Optional[date], endDate: Optional[date]
) -> FinancialReportResponse:
    """
    Retrieves comprehensive financial reports using data from QuickBooks, Sales Tracking, and
    Inventory Management modules. This route compiles and presents financial data which includes
    sales, expenses, and profitability analytics. The expected response would be detailed JSON
    containing various financial indicators and their breakdowns. This integration ensures data
    accuracy and coherence across related modules.

    Args:
        startDate (Optional[date]): Start date for the financial report period, format YYYY-MM-DD.
        endDate (Optional[date]): End date for the financial report period, format YYYY-MM-DD.

    Returns:
        FinancialReportResponse: Contains structured financial data including sale totals, expense totals,
        profitability metrics, and related breakdowns.

    Example:
        response = await getFinancialReports(date(2023, 1, 1), date(2023, 1, 31))
        print(response)
    """
    sales_breakdown = {}
    expense_breakdown = {}
    total_sales = 0.0
    total_expenses = 0.0
    startDateTime = (
        datetime.combine(startDate, datetime.min.time()) if startDate else None
    )
    endDateTime = datetime.combine(endDate, datetime.max.time()) if endDate else None
    transactions = await prisma.models.Transaction.prisma().find_many(
        where={"date": {"gte": startDateTime, "lte": endDateTime}}
    )
    for transaction in transactions:
        if (
            transaction.type == prisma.enums.TransactionType.Sale
            and transaction.inventoryItem
        ):
            total_sales += transaction.amount
            category = transaction.inventoryItem.type.value
            sales_breakdown[category] = (
                sales_breakdown.get(category, 0) + transaction.amount
            )
        elif transaction.type == prisma.enums.TransactionType.Expense:
            total_expenses += transaction.amount
            expense_breakdown["General"] = (
                expense_breakdown.get("General", 0) + transaction.amount
            )
    profitability = total_sales - total_expenses
    response = FinancialReportResponse(
        totalSales=total_sales,
        totalExpenses=total_expenses,
        profitability=profitability,
        salesBreakdown=sales_breakdown,
        expenseBreakdown=expense_breakdown,
    )
    return response
