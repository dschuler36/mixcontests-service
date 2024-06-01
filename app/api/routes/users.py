from fastapi import APIRouter, Depends, Request

from app import deps
from app.api import schemas
from app.api.services.users_service import UsersService

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/users", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.create_user(user)


@router.post("/users/clerk/webhook")
def sync_webhook_data(
        request: Request,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.handle_webhook_sync(request)
