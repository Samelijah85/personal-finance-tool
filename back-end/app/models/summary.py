from pydantic import BaseModel


class Summary(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
