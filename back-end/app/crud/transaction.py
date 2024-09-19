from bson import ObjectId
from datetime import datetime

from fastapi import HTTPException
from pymongo import ReturnDocument

from ..models.transaction import Transaction, TransactionInDB, Category
from ..core.db import transaction_collection
from ..schemas.transaction import transactionEntity, transactionsEntity


def read_transactions(
    username: str, startDate: datetime | None = None, endDate: datetime | None = None, category: Category | None = None
) -> list[TransactionInDB]:
    """Fetch all transactions for the current user."""
    transaction_query = {"user": username}
    if startDate and endDate:
        transaction_query["date"] = {"$gte": startDate, "$lte": endDate}
    elif startDate:
        transaction_query["date"] = {"$gte": startDate}
    elif endDate:
        transaction_query["date"] = {"$lte": endDate}
    if category:
        transaction_query["category"] = category.value

    transactions = transactionsEntity(transaction_collection.find(transaction_query).sort("date", -1))
    return transactions


def read_transaction_by_id(id: str) -> TransactionInDB:
    """Fetch a transaction by ID."""
    try:
        transaction = transaction_collection.find_one({"_id": ObjectId(id)})
        return transactionEntity(transaction)
    except Exception:
        raise HTTPException(status_code=404, detail="Transaction not found")


def write_transaction(username: str, transaction: Transaction) -> TransactionInDB:
    """Create a new transaction."""
    transaction_dict = transaction.model_dump()
    transaction_dict["user"] = username
    result = transaction_collection.insert_one(transaction_dict)
    inserted_transaction = transaction_collection.find_one({"_id": ObjectId(result.inserted_id)})
    return transactionEntity(inserted_transaction)


def update_transaction(username: str, id: str, transaction: Transaction) -> TransactionInDB:
    """Update an existing transaction."""
    transaction_dict = transaction.model_dump()
    transaction_dict["user"] = username
    try:
        updated_transaction = transaction_collection.find_one_and_update(
            filter={"_id": ObjectId(id)},
            update={"$set": transaction_dict},
            return_document=ReturnDocument.AFTER
        )
        return transactionEntity(updated_transaction)
    except Exception:
        raise HTTPException(status_code=404, detail="Transaction not found")


def delete_transaction(id: str) -> dict:
    """Delete a transaction by ID."""
    try:
        if transaction_collection.find_one_and_delete({"_id": ObjectId(id)}):
            return {"message": "Transaction deleted"}
    except Exception:
        raise HTTPException(status_code=404, detail="Transaction not found")


def delete_all_transactions(username: str) -> dict:
    """Delete all transactions."""
    transaction_collection.delete_many({"user": username})
    return {"message": "All transactions deleted"}