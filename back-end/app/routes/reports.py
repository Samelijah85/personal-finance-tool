from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from ..core.db import transaction_collection
from ..models.user import User
from ..models.summary import Summary
from ..crud.user import get_current_user
from ..schemas.transaction import transactionsEntity

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={
        404: {"description": "Not found"},
    },
)


@router.get("/summary")
async def read_transaction_summary(
    user: Annotated[User, Depends(get_current_user)], startDate: datetime | None = None, endDate: datetime | None = None
) -> Summary:
    """Get a summary report of income vs. expenses."""
    report_query = {"user": user.username}
    if startDate and endDate:
        report_query["date"] = {"$gte": startDate, "$lte": endDate}
    elif startDate:
        report_query["date"] = {"$gte": startDate}
    elif endDate:
        report_query["date"] = {"$lte": endDate}

    transactions = transactionsEntity(transaction_collection.find(report_query))
    total_income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.category == "income"
    )
    total_expenses = sum(
        transaction.amount
        for transaction in transactions
        if transaction.category == "expense"
    )
    return Summary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_savings=total_income-total_expenses
    )
