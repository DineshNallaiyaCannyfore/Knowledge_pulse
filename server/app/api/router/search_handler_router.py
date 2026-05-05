from fastapi import APIRouter, Depends
from app.api.services.search_handler_service import search_service
from requests import Session
from app.db.database import get_session
from app.api.schemas.search_handler_models import (
    searchSchemaRequest,
    searchSchemaResponce,
)

router = APIRouter(prefix="/search", tags=["query"])


@router.post("/find", status_code=201, response_model=searchSchemaResponce)
def search_router(body: searchSchemaRequest, db: Session = Depends(get_session)):
    return search_service(body.query, db)
