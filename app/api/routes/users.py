from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import deps
from app.api import schemas, models
from app.api.database import get_db
from app.api.services.users_service import UsersService

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        users_service: UsersService = Depends(deps.get_users_service)
):
    return users_service.create_user(user)