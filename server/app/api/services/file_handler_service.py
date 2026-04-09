import os
from typing import List
from fastapi import UploadFile
from requests import Session
from app.db.models import FileStorage
from app.core.constants import FILE_DIRECTROY

os.makedirs(FILE_DIRECTROY, exist_ok=True)


def file_uploader(files: List[UploadFile], db: Session):
    for file in files:
        file_path = os.path.join(FILE_DIRECTROY, file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        insert_file = FileStorage(file_name=file.filename, file_path=file_path)
        db.add(insert_file)
        db.commit()
        db.refresh(insert_file)
        return {"message": "Successfully file uploaded."}
