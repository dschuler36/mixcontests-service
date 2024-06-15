from fastapi import APIRouter, Depends

from app import deps
from app.api import schemas
from app.api.services.contest_results_service import ContestResultsService
from app.api.services.contests_service import ContestsService

router = APIRouter(prefix="/api", tags=["contest_results"])


@router.get("/contest_results/{contest_id}")
def get_results_for_contest_id(
        contest_id: int,
        contest_results_service: ContestResultsService = Depends(deps.get_contest_results_service)):
    return contest_results_service.get_results_for_contest_id(contest_id)