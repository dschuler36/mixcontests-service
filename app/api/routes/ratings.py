from fastapi import APIRouter, Depends

from app import deps
from app.api import schemas
from app.api.services.ratings_service import RatingsService

router = APIRouter(prefix="/api", tags=["ratings"])


@router.post("/ratings", response_model=schemas.Rating)
def create_rating(
        rating: schemas.RatingCreate,
        ratings_service: RatingsService = Depends(deps.get_ratings_service)):
    return ratings_service.create_rating(rating)
