from ..models.transaction import TransactionInDB, Category


def transactionEntity(item) -> TransactionInDB:
    return TransactionInDB(
        id=str(item["_id"]),
        amount=item["amount"],
        category=Category.expense if item["category"] == "Expense" else Category.income,
        date=item["date"],
        description=item["description"],
    )


def transactionsEntity(entity) -> list[TransactionInDB]:
    return [transactionEntity(item) for item in entity]
