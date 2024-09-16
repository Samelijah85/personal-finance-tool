from datetime import datetime
from bson import ObjectId
from typing import Annotated
from bson.errors import InvalidId

from fastapi import APIRouter, HTTPException, Depends
from pymongo import ReturnDocument

from ..schemas.budget import budgetEntity, budgetsEntity
from ..core.db import budget_collection
from ..models.user import User
from ..models.budget import Budget, BudgetInDB, BudgetBreakdown, FullBudget
from ..crud.user import get_current_user
from ..crud.report import read_transaction_summary

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"],
    responses={
        404: {"description": "Not found"},
        201: {"description": "Created"},
    },
)


@router.get("/")
async def read_budgets(
    user: Annotated[User, Depends(get_current_user)], startDate: datetime | None = None, endDate: datetime | None = None
) -> list[BudgetInDB]:
    """Fetch all budgets for the current user."""
    budget_query = {"user": user.username}
    if startDate and endDate:
        budget_query["date"] = {"$gte": startDate, "$lte": endDate}
    elif startDate:
        budget_query["date"] = {"$gte": startDate}
    elif endDate:
        budget_query["date"] = {"$lte": endDate}

    budgets = budgetsEntity(budget_collection.find(budget_query))
    return budgets


@router.get("/{id}")
async def read_budget(id: str, user: Annotated[User, Depends(get_current_user)]) -> FullBudget:
    """Fetch a budget by ID."""
    try:
        budget = budgetEntity(budget_collection.find_one({"_id": ObjectId(id)}))
        summary = read_transaction_summary(user.username, budget.start_date, budget.end_date)
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


@router.post("/", status_code=201)
async def create_budget(budget: Budget, user: Annotated[User, Depends(get_current_user)]) -> BudgetInDB:
    """Create a new budget."""
    budget_dict = budget.model_dump()
    budget_dict["user"] = user.username
    result = budget_collection.insert_one(budget_dict)
    inserted_budget = budget_collection.find_one({"_id": ObjectId(result.inserted_id)})
    return budgetEntity(inserted_budget)


@router.put("/{id}")
async def update_budget(id: str, budget: Budget, user: Annotated[User, Depends(get_current_user)]) -> BudgetInDB:
    """Update an existing budget."""
    budget_dict = budget.model_dump()
    budget_dict["user"] = user.username
    try:
        updated_budget = budget_collection.find_one_and_update(
            filter={"_id": ObjectId(id)},
            update={"$set": budget_dict},
            return_document=ReturnDocument.AFTER
        )
        return budgetEntity(updated_budget)
    except Exception:
        raise HTTPException(status_code=404, detail="Budget not found")


@router.delete("/{id}")
async def delete_budget(id: str, user: Annotated[User, Depends(get_current_user)]) -> dict:
    """Delete a budget by ID."""
    try:
        if budget_collection.find_one_and_delete({"_id": ObjectId(id)}):
            return {"message": "Budget deleted"}
    except Exception:
        raise HTTPException(status_code=404, detail="Budget not found")


@router.delete("/")
async def delete_all_budgets(user: Annotated[User, Depends(get_current_user)]) -> dict:
    """Delete all budgets."""
    budget_collection.delete_many({"user": user.username})
    return {"message": "All budgets deleted"}
