import json
from typing import Any, Dict

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app import deps
from app.api import schemas
from app.api.services.users_service import UsersService

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/users")
def get_user(
        idp_user_id: str,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.get_user_by_id(idp_user_id)


@router.post("/users", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.create_user(user)


@router.post("/users/clerk/webhook")
async def sync_webhook_data(
        request: Request,
        users_service: UsersService = Depends(deps.get_users_service)):
    try:
        return await users_service.handle_webhook_sync(request)
    except Exception as e:
        print(f"Error processing webhook data: {e}")
        raise e
