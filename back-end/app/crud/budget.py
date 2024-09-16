from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

from fastapi import HTTPException
from pymongo import ReturnDocument

from ..schemas.budget import budgetEntity, budgetsEntity
from ..core.db import budget_collection
from ..models.budget import Budget, BudgetInDB, BudgetBreakdown, FullBudget
from ..crud.report import read_transaction_summary


def read_budgets(
    username: str, startDate: datetime | None = None, endDate: datetime | None = None
) -> list[BudgetInDB]:
    """Fetch all budgets for the current user."""
    budget_query = {"user": username}
    if startDate and endDate:
        budget_query["date"] = {"$gte": startDate, "$lte": endDate}
    elif startDate:
        budget_query["date"] = {"$gte": startDate}
    elif endDate:
        budget_query["date"] = {"$lte": endDate}

    budgets = budgetsEntity(budget_collection.find(budget_query))
    return budgets


def read_budget_by_id(id: str, username: str) -> FullBudget:
    """Fetch a budget by ID."""
    try:
        budget = budgetEntity(budget_collection.find_one({"_id": ObjectId(id)}))
        summary = read_transaction_summary(username, budget.start_date, budget.end_date)
        print("before limit")

        limit = float(budget.limit_amount,)
        expenses = float(summary.total_expenses)
        balance = limit - expenses
        breakdown = BudgetBreakdown(
            limit_amount=limit,
            used_amount=expenses,
            balance=balance,
            percentage=expenses / limit * 100.0
        )
        return FullBudget(budget=budget, breakdown=breakdown)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Budget not found")


def write_budget(budget: Budget, username: str) -> BudgetInDB:
    """Create a new budget."""
    budget_dict = budget.model_dump()
    budget_dict["user"] = username
    result = budget_collection.insert_one(budget_dict)
    inserted_budget = budget_collection.find_one({"_id": ObjectId(result.inserted_id)})
    return budgetEntity(inserted_budget)


def update_budget(id: str, budget: Budget, username: str) -> BudgetInDB:
    """Update an existing budget."""
    budget_dict = budget.model_dump()
    budget_dict["user"] = username
    try:
        updated_budget = budget_collection.find_one_and_update(
            filter={"_id": ObjectId(id)},
            update={"$set": budget_dict},
            return_document=ReturnDocument.AFTER
        )
        return budgetEntity(updated_budget)
    except Exception:
        raise HTTPException(status_code=404, detail="Budget not found")


def delete_budget(id: str) -> dict:
    """Delete a budget by ID."""
    try:
        if budget_collection.find_one_and_delete({"_id": ObjectId(id)}):
            return {"message": "Budget deleted"}
    except Exception:
        raise HTTPException(status_code=404, detail="Budget not found")


def delete_all_budgets(username: str) -> dict:
    """Delete all budgets."""
    budget_collection.delete_many({"user": username})
    return {"message": "All budgets deleted"}
