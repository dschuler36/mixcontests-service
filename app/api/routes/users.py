import json
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app import deps
from app.api import schemas
from app.api.services.users_service import UsersService

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/users")
def get_user(
        user_id: UUID,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.get_user_by_id(user_id)


@router.post("/users", response_model=schemas.User)
def create_user(
        user: schemas.UserBase,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.create_user(user)


@router.get("/users/{user_id}/contests")
def get_unique_contests_entered(
        user_id: UUID,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.get_unique_contests_entered(user_id)


@router.get("/users/{user_id}/feedback_count")
def get_ratings_given(
        user_id: UUID,
        users_service: UsersService = Depends(deps.get_users_service)):
    return users_service.get_feedback_given(user_id)

# @router.post("/users/clerk/webhook")
# async def sync_webhook_data(
#         request: Request,
#         users_service: UsersService = Depends(deps.get_users_service)):
#     try:
#         return await users_service.handle_webhook_sync(request)
#     except Exception as e:
#         print(f"Error processing webhook data: {e}")
#         raise e
