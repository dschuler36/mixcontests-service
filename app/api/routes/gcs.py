from fastapi import APIRouter, Depends, Path, UploadFile, File

from app import deps
from app.api.services.gcs_service import GCSService

router = APIRouter(prefix="/api", tags=["gcs"])


@router.get("/download/{file_path:path}")
def create_rating(
        file_path: str = Path(..., min_length=1),
        gcs_service: GCSService = Depends(deps.get_gcs_service)):
    return gcs_service.download_file(file_path)


@router.post("/upload/{contest_id}/submissions/{submission_id}")
async def upload_file(
        contest_id: int,
        submission_id: int,
        file: UploadFile = File(...),
        gcs_service: GCSService = Depends(deps.get_gcs_service)):
    destination_path = f"{contest_id}/submissions/{submission_id}/"
    return gcs_service.upload_file(file, destination_path)


@router.get("/generate_signed_url/{file_name:path}")
async def generate_signed_url(
        file_name: str = Path(..., min_length=1),
        gcs_service: GCSService = Depends(deps.get_gcs_service)):
    return await gcs_service.generate_signed_url(file_name)
