from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import schemas, models
from app.api.database import get_db

router = APIRouter()


@router.post("/stems/", response_model=schemas.Stem)
def create_stem(stem: schemas.StemCreate, db: Session = Depends(get_db)):
    db_stem = models.Stem(**stem.dict())
    db.add(db_stem)
    db.commit()
    db.refresh(db_stem)
    return db_stem
