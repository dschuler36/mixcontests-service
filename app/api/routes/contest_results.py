from fastapi import APIRouter, Depends

from app import deps
from app.api import schemas
from app.api.services.contest_results_service import ContestResultsService
from app.api.services.contests_service import ContestsService

router = APIRouter(prefix="/api", tags=["contest_results"])


@router.get("/contest_results/{contest_id}/summary")
async def get_contest_results_summary_for_contest_id(
        contest_id: int,
        contest_results_service: ContestResultsService = Depends(deps.get_contest_results_service)):
    return await contest_results_service.get_contest_results_summary_for_contest_id(contest_id)
