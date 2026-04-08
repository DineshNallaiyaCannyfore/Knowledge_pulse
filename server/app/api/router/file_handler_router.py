from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from requests import Session
from app.db.database import sessionLocal
from app.api.schemas.file_handler_schema import FileHandlerSchema
from app.api.services.file_handler_service import file_uploader

router = APIRouter(prefix="/files", tags=["fileupload"])


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=List[FileHandlerSchema], status_code=201)
def file_handler(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    return file_uploader(files, db)
