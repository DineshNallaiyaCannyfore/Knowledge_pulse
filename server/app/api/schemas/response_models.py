from pydantic import BaseModel


class UploadResponseModel(BaseModel):
    message: str


class FileListItemModel(BaseModel):
    id: int
    file_name: str
    file_path: str


class FileHandlerResponseModel(BaseModel):
    files: list[FileListItemModel]
