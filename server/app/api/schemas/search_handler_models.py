from pydantic import BaseModel


class searchSchemaRequest(BaseModel):
    query: str


class searchSchemaResponce(BaseModel):
    llm_answer: str
    source_document: str
