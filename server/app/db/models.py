from app.db.database import Base
from sqlalchemy import String, Column, JSON, Integer, Text, UniqueConstraint, ForeignKey
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship


class FileStorage(Base):
    __tablename__ = "knowledge_puls"
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    chunks = relationship("DocumentChunk", back_populates="file")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(384))
    extra_metadata = Column(JSON)
    file_id = Column(Integer, ForeignKey("knowledge_puls.id"))
    file = relationship("FileStorage", back_populates="chunks")
    __table_args__ = (UniqueConstraint("content", name="unique_chunk"),)
