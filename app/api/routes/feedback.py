from fastapi import APIRouter, Depends

from app import deps
from app.api import schemas
from app.api.services.feedback_service import FeedbackService

router = APIRouter(prefix="/api", tags=["feedback"])


@router.post("/feedback")
def create_rating(
        feedback: schemas.FeedbackCreate,
        feedback_service: FeedbackService = Depends(deps.get_feedback_service)):
    return feedback_service.create_feedback(feedback)

@router.get("/feedback/{feedback_id}")
def get_feedback_by_id(
        feedback_id: int,
        feedback_service: FeedbackService = Depends(deps.get_feedback_service)):
    return feedback_service.get_feedback_by_id(feedback_id)


@router.get("/feedback/{contest_id}/submissions")
def get_head_to_head_mixes(
        contest_id: int,
        feedback_service: FeedbackService = Depends(deps.get_feedback_service)):
    return feedback_service.get_head_to_head_mixes(contest_id)