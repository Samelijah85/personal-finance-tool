from fastapi import APIRouter

from ..crud.user import get_all_users


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    """Fetch all users."""
    all_users = get_all_users()
    return all_users