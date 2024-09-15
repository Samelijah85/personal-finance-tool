from datetime import datetime

from pydantic import BaseModel

class Budget(BaseModel):
    limit_amount: float
    description: str
    start_date: datetime
    end_date: datetime


class BudgetInDB(Budget):
    id: str
