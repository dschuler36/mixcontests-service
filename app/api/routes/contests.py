from fastapi import APIRouter, Depends

from app import deps
from app.api import schemas
from app.api.services.contests_service import ContestsService

router = APIRouter(prefix="/api", tags=["contests"])


@router.get("/contests")
async def get_all_contests(contests_service: ContestsService = Depends(deps.get_contests_service)):
    return await contests_service.get_all_contests()


@router.get("/contests/active")
async def get_active_contest(
        contests_service: ContestsService = Depends(deps.get_contests_service)):
    return await contests_service.get_active_contest()


@router.get("/contests/{contest_id}")
async def get_contest_by_id(
        contest_id: int,
        contests_service: ContestsService = Depends(deps.get_contests_service)):
    return await contests_service.get_contest_by_id(contest_id)


@router.post("/contests", response_model=schemas.Contest)
async def create_contest(
        contest: schemas.ContestCreate,
        contests_service: ContestsService = Depends(deps.get_contests_service)):
    return await contests_service.create_contest(contest)


@router.put("/contests/{contest_id}")
async def update_contest(
        contest_id: int,
        contest: schemas.ContestUpdate,
        contests_service: ContestsService = Depends(deps.get_contests_service)
):
    return await contests_service.update_contest(contest_id, contest)


@router.delete("/contests/{contest_id}")
async def delete_contest(
        contest_id: int,
        contests_service: ContestsService = Depends(deps.get_contests_service)
):
    return await contests_service.delete_contest(contest_id)
