from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from ..models.transaction import Transaction, TransactionInDB, Category
from ..models.user import User
from ..crud.user import get_current_user
from ..crud.transaction import (
    read_transactions,
    read_transaction_by_id,
    write_transaction,
    update_transaction as put_transaction,
    delete_transaction as remove_transaction,
    delete_all_transactions as clear_all_transactions
)

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={
        404: {"description": "Not found"},
        201: {"description": "Created"},
    },
)


@router.get("/")
async def get_all_transactions(
    user: Annotated[User, Depends(get_current_user)], startDate: datetime | None = None, endDate: datetime | None = None, category: Category | None = None
) -> list[TransactionInDB]:
    """Fetch all transactions for the current user."""
    return read_transactions(user.username, startDate, endDate, category)


@router.get("/{id}")
async def get_transaction_by_id(id: str, user: Annotated[User, Depends(get_current_user)]) -> TransactionInDB:
    """Fetch a transaction by ID."""
    return read_transaction_by_id(id)


@router.post("/", status_code=201)
async def create_transaction(transaction: Transaction, user: Annotated[User, Depends(get_current_user)]) -> TransactionInDB:
    """Create a new transaction."""
    return write_transaction(user.username, transaction)


@router.put("/{id}")
async def update_transaction(id: str, transaction: Transaction, user: Annotated[User, Depends(get_current_user)]) -> TransactionInDB:
    """Update an existing transaction."""
    return put_transaction(user.username, id, transaction)


@router.delete("/{id}")
async def delete_transaction(id: str, user: Annotated[User, Depends(get_current_user)]) -> dict:
    """Delete a transaction by ID."""
    return remove_transaction(id)


@router.delete("/")
async def delete_all_transactions(user: Annotated[User, Depends(get_current_user)]) -> dict:
    """Delete all transactions."""
    return clear_all_transactions(user.username)
