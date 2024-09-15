from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class Category(str, Enum):
    income = "income"
    expense = "expense"


class Transaction(BaseModel):
    amount: float
    category: Category
    date: datetime
    description: str


class TransactionInDB(Transaction):
    id: str
