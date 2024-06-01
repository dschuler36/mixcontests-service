from fastapi import APIRouter, Depends

from app import deps
from app.api import schemas
from app.api.services.submissions_service import SubmissionsService

router = APIRouter(prefix="/api", tags=["submissions"])


@router.get("/submissions/{submission_id}")
def get_submission_by_id(
        submission_id: int,
        submissions_service: SubmissionsService = Depends(deps.get_submissions_service)):
    return submissions_service.get_submission_by_id(submission_id)


@router.post("/submissions", response_model=schemas.Submission)
def create_submission(
        submission: schemas.SubmissionCreate,
        submissions_service: SubmissionsService = Depends(deps.get_submissions_service)):
    return submissions_service.create_submission(submission)


@router.get("/submissions/{user_id}/{contest_id}")
def get_submission_by_user_and_contest(
        user_id: int,
        contest_id: int,
        submissions_service: SubmissionsService = Depends(deps.get_submissions_service)):
    return submissions_service.get_submission_by_user_and_contest(user_id, contest_id)