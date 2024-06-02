from fastapi import HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session
from svix import Webhook, WebhookVerificationError

from app.api import models
from app.api.config import settings
from app.api.schemas import UserCreatedEvent, UserUpdatedEvent, UserDeletedEvent


class UsersService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, idp_user_id):
        user = self.db.query(models.User).filter(models.User.idp_user_id == idp_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, idp_user_id: str, email: str, username: str):
        db_user = models.User(idp_user_id=idp_user_id, email=email, username=username)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, idp_user_id: str, email: str = None, username: str = None):
        user = self.get_user_by_id(idp_user_id)
        if email:
            user.email = email
        if username:
            user.username = username
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, idp_user_id: str):
        user = self.get_user_by_id(idp_user_id)
        self.db.delete(user)
        self.db.commit()
        return user

    async def handle_webhook_sync(self, request):
        payload = await request.body()
        headers = request.headers
        try:
            wh = Webhook(settings.WEBHOOK_SECRET)
            msg = wh.verify(payload, headers)
        except WebhookVerificationError as e:
            raise HTTPException(status_code=400, detail="Webhook verification failed")

        data = await request.json()
        event_type = data.get('type')

        try:
            if event_type == 'user.created':
                print('Processing user creation event', data)
                event = UserCreatedEvent.parse_obj(data)
                user_id = event.data.id
                email = event.data.email_addresses[0].email_address
                username = event.data.username
                self.create_user(user_id, email, username)

            elif event_type == 'user.updated':
                print('Processing user updated event', data)
                event = UserUpdatedEvent.parse_obj(data)
                user_id = event.data.id
                email = event.data.email_addresses[0].email_address if event.data.email_addresses else None
                username = event.data.username
                self.update_user(user_id, email, username)

            elif event_type == 'user.deleted':
                print('Processing user deleted event', data)
                event = UserDeletedEvent.parse_obj(data)
                user_id = event.data.id
                self.delete_user(user_id)

        except ValidationError as e:
            raise HTTPException(status_code=422, detail=str(e))

        return {"message": "Event processed"}
