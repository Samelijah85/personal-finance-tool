from ..models.budget import BudgetInDB

def budgetEntity(item) -> BudgetInDB:
    return BudgetInDB(
        id=str(item["_id"]),
        limit_amount=item["limit_amount"],
        description=item["description"],
        start_date=item["start_date"],
        end_date=item["end_date"]
    )


def budgetsEntity(entity) -> list[BudgetInDB]:
    return [budgetEntity(item) for item in entity]
