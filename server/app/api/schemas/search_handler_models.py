from pydantic import BaseModel
from typing import List, Optional


class searchSchemaRequest(BaseModel):
    query: str


class searchSchemaResponse(BaseModel):
    llm_answer: str
    source_document: Optional[List[str]] = None
