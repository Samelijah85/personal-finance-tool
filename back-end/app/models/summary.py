from pydantic import BaseModel, field_validator


class Summary(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float

    @field_validator("total_income", "total_expenses", "net_saving", check_fields=False)
    def round_money(cls, value):
        return round(value, 2)
