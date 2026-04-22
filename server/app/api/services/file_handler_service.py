import os
from io import BytesIO
from typing import List
from fastapi import UploadFile
from requests import Session
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from docx import Document
from sqlalchemy.exc import IntegrityError
from app.core.constants import FILE_DIRECTROY, PDF, MODEL_NAME, DOCX
from app.db.models import FileStorage, DocumentChunk


os.makedirs(FILE_DIRECTROY, exist_ok=True)

embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)


async def file_uploader(files: List[UploadFile], db: Session):
    for file in files:
        file_path = os.path.join(FILE_DIRECTROY, file.filename)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        texts = await text_extraction(content, file.filename)
        chunks = await text_split(texts)
        chunk_texts = [c["content"] for c in chunks]
        embedded_text = get_embedding(chunk_texts)
        insert_file = FileStorage(
            file_name=file.filename,
            file_path=file_path,
        )
        try:
            db.add(insert_file)
            db.commit()
            db.refresh(insert_file)

            for i, chunk in enumerate(chunks):
                db.add(
                    DocumentChunk(
                        content=chunk["content"],
                        embedding=embedded_text[i],
                        file_id=insert_file.id,
                        extra_metadata={
                            "file_name": file.filename,
                            "chunk_id": i,
                            "page": chunk["page"],
                        },
                    )
                )
            db.commit()
        except IntegrityError:
            db.rollback()
            return {"message": "Duplicate data found"}

        return {"message": "Successfully file uploaded."}


async def text_extraction(content, filename):
    documents = []
    file_format = filename.split(".")[1]

    if file_format == PDF:
        reader = PdfReader(BytesIO(content))
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                documents.append({"text": page_text, "page": page_num + 1})

    elif file_format == DOCX:
        doc = Document(BytesIO(content))
        for i, para in enumerate(doc.paragraphs):
            if para.text:
                documents.append({"text": para.text, "page": i + 1})

    return documents


async def text_split(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    final_chunks = []

    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        for chunk in chunks:
            final_chunks.append({"content": chunk, "page": doc["page"]})

    return final_chunks


def get_embedding(chunks):
    return embedding_model.embed_documents(chunks)


async def get_file_lists(db: Session):
    files = db.query(FileStorage).all()
    return {"files": files}
