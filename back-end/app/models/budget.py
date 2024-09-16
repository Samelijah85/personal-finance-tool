from datetime import datetime

from pydantic import BaseModel, field_validator

class Budget(BaseModel):
    limit_amount: float
    description: str
    start_date: datetime
    end_date: datetime

    @field_validator("limit_amount", check_fields=False)
    def round_money(cls, value):
        return round(value, 2)


class BudgetInDB(Budget):
    id: str


class BudgetBreakdown(BaseModel):
    limit_amount: float
    used_amount: float
    balance: float
    percentage: float

    @field_validator("limit_amount", "used_amount", "balance", "percentage")
    def round_values(cls, value):
        return round(value, 2)


class FullBudget(BaseModel):
    budget: BudgetInDB
    breakdown: BudgetBreakdown
