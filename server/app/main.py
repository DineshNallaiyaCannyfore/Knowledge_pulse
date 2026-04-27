from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.router.file_handler_router import router as file_handler
from app.api.router.search_handler_router import router as search_handler

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(file_handler)
app.include_router(search_handler)


@app.get("/")
def read_root():
    return {"message": "Welcome to Knowledge Pulse API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
