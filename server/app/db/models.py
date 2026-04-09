from app.db.database import Base
from sqlalchemy import String, Column, Integer


class FileStorage(Base):
    __tablename__ = "knowledge_puls"
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
