from fastapi import APIRouter, Depends, Path

from app import deps
from app.api.services.gcs_service import GCSService

router = APIRouter(prefix="/api", tags=["gcs"])


@router.get("/download/{file_path:path}")
def create_rating(
        file_path: str = Path(..., min_length=1),
        gcs_service: GCSService = Depends(deps.get_gcs_service)):
    return gcs_service.download_file(file_path)
