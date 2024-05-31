from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app import deps
from app.api import schemas
from app.api.auth import auth_scheme
from app.api.services.users_service import UsersService

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/users/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        users_service: UsersService = Depends(deps.get_users_service),
        token: HTTPBearer = Depends(auth_scheme)
):
    return users_service.create_user(user)

# @app.route("/login")
# def login():
#     return oauth.auth0.authorize_redirect(
#         redirect_uri=url_for("callback", _external=True)
#     )