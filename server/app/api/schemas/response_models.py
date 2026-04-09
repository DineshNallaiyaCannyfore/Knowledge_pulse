from pydantic import BaseModel


class UploadResponseModel(BaseModel):
    message: str
