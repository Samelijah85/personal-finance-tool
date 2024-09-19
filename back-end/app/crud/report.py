from datetime import datetime

from ..models.summary import Summary
from ..models.transaction import Category
from ..crud.transaction import read_transactions


def read_transaction_summary(
    username: str, startDate: datetime | None = None, endDate: datetime | None = None
) -> Summary:
    """Get a summary report of income vs. expenses."""
    transactions = read_transactions(username=username, startDate=startDate, endDate=endDate)
    total_income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.category == Category.income
    )
    total_expenses = sum(
        transaction.amount
        for transaction in transactions
        if transaction.category == Category.expense
    )
    return Summary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_savings=total_income-total_expenses
    )