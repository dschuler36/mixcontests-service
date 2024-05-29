from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import deps
from app.api import schemas, models
from app.api.services.contests_service import ContestsService

router = APIRouter()


@router.get("/contests/")
def get_all_contests(contests_service: ContestsService = Depends(deps.get_contests_service)):
    return contests_service.get_all_contests()


@router.get("/contests/{contest_id}")
def get_contest_by_id(
        contest_id: int,
        contests_service: ContestsService = Depends(deps.get_contests_service)):
    return contests_service.get_contest_by_id(contest_id)


@router.post("/contests/", response_model=schemas.Contest)
def create_contest(
        contest: schemas.ContestCreate,
        contests_service: ContestsService = Depends(deps.get_contests_service)):
    return contests_service.create_contest(contest)
