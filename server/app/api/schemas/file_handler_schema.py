from pydantic import BaseModel


class FileHandlerSchema(BaseModel):
    message: str
