from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from requests import Session
from app.db.database import get_session
from app.api.schemas.response_models import UploadResponseModel
from app.api.services.file_handler_service import file_uploader

router = APIRouter(prefix="/files", tags=["fileupload"])


@router.post("/upload", response_model=UploadResponseModel, status_code=201)
async def file_handler(
    files: List[UploadFile] = File(...), db: Session = Depends(get_session)
):
    return await file_uploader(files, db)
