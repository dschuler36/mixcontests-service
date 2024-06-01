from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.api import models
from app.api import schemas
import hmac
import hashlib
from app.api.config import settings


class UsersService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.UserCreate):
        db_user = models.User(username=user.username, email=user.email, password_hash=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    @staticmethod
    async def verify_signature(request: Request):
        signature = request.headers.get('clerk-signature')
        body = await request.body()
        if signature is None or body is None:
            raise HTTPException(status_code=400, detail="Invalid signature or body")

        computed_signature = hmac.new(
            settings.WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(computed_signature, signature):
            raise HTTPException(status_code=400, detail="Invalid signature")

    async def handle_webhook_sync(self, request: Request):
        try:
            await self.verify_signature(request)
        except Exception as e:
            return {"error": str(e)}

        event = await request.json()
        event_type = event.get('type')

        if event_type == 'user.created':
            # Handle user creation event
            user_id = event['data']['id']
            # Add logic to sync with your database
            print(f"User created: {user_id}")

        elif event_type == 'user.updated':
            # Handle user update event
            user_id = event['data']['id']
            # Add logic to sync with your database
            print(f"User updated: {user_id}")

        elif event_type == 'user.deleted':
            # Handle user deletion event
            user_id = event['data']['id']
            # Add logic to sync with your database
            print(f"User deleted: {user_id}")

        return {"message": "Event received"}
