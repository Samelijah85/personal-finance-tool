from enum import Enum
from datetime import datetime

from pydantic import BaseModel, field_validator


class Category(str, Enum):
    income = "Income"
    expense = "Expense"


class Transaction(BaseModel):
    amount: float
    category: Category
    date: datetime
    description: str

    @field_validator("amount", check_fields=False)
    def round_money(cls, value):
        return round(value, 2)


class TransactionInDB(Transaction):
    id: str
