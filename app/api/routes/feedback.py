from uuid import UUID

from fastapi import APIRouter, Depends

from app import deps
from app.api import schemas
from app.api.services.feedback_service import FeedbackService

router = APIRouter(prefix="/api", tags=["feedback"])


@router.post("/feedback")
async def create_rating(
        feedback: schemas.FeedbackCreate,
        feedback_service: FeedbackService = Depends(deps.get_feedback_service)):
    return await feedback_service.create_feedback(feedback)


@router.get("/feedback/{feedback_id}")
async def get_feedback_by_id(
        feedback_id: int,
        feedback_service: FeedbackService = Depends(deps.get_feedback_service)):
    return await feedback_service.get_feedback_by_id(feedback_id)


@router.get("/feedback/{contest_id}/submissions/{user_id}")
async def get_head_to_head_mixes(
        contest_id: int,
        user_id: UUID,
        feedback_service: FeedbackService = Depends(deps.get_feedback_service)):
    return await feedback_service.get_head_to_head_mixes(contest_id, user_id)


@router.get("/feedback/{contest_id}/count/{user_id}")
def get_head_to_head_mixes(
        contest_id: int,
        user_id: UUID,
        feedback_service: FeedbackService = Depends(deps.get_feedback_service)):
    return feedback_service.get_count_feedback_submitted(contest_id, user_id)
