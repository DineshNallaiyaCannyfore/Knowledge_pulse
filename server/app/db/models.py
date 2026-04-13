from app.db.database import Base
from sqlalchemy import String, Column, JSON, Integer, Text, UniqueConstraint
from pgvector.sqlalchemy import Vector


class FileStorage(Base):
    __tablename__ = "knowledge_puls"
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(384))
    extra_metadata = Column(JSON)
    __table_args__ = (UniqueConstraint("content", name="unique_chunk"),)
