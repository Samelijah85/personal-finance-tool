from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from ..models.user import User
from ..models.summary import Summary
from ..crud.user import get_current_user
from ..crud.report import read_transaction_summary

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={
        404: {"description": "Not found"},
    },
)


@router.get("/summary")
async def get_transaction_summary(
    user: Annotated[User, Depends(get_current_user)], startDate: datetime | None = None, endDate: datetime | None = None
) -> Summary:
    """Get a summary report of income vs. expenses."""
    return read_transaction_summary(user.username, startDate, endDate)
