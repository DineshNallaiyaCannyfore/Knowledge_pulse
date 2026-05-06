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
from pathlib import Path

os.makedirs(FILE_DIRECTROY, exist_ok=True)

embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)


async def file_uploader(files: List[UploadFile], db: Session):
    errors = []
    for file in files:
        try:
            file_path = os.path.join(FILE_DIRECTROY, file.filename)
            content = await file.read()

            with open(file_path, "wb") as f:
                f.write(content)

            texts = await text_extraction(content, file.filename)
            if "error" in texts:
                errors.append(
                    f"Error extracting text from {file.filename}: {texts['error']}"
                )
                return

            chunks = await text_split(texts)
            chunk_texts = [c["content"] for c in chunks]
            embedded_text = get_embedding(chunk_texts)

            insert_file = FileStorage(
                file_name=file.filename,
                file_path=file_path,
            )

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
            errors.append(f"Duplicate data found for {file.filename}")
        except Exception as e:
            db.rollback()
            errors.append(f"Error uploading {file.filename}: {str(e)}")

    return {
        "message": "Files uploaded successfully.",
        "errors": errors if errors else None,
    }


async def text_extraction(content, filename):
    documents = []
    file_format = Path(filename).suffix.lstrip(".").lower()

    if not file_format:
        return {"error": "File format could not be determined."}

    if file_format == PDF:
        reader = PdfReader(BytesIO(content))
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text.strip():
                documents.append({"text": page_text, "page": page_num + 1})

    elif file_format == DOCX:
        doc = Document(BytesIO(content))
        current_text = []
        page_num = 1

        for para in doc.paragraphs:
            if para.text.strip():
                current_text.append(para.text)

        if current_text:
            combined_text = "\n".join(current_text)
            if combined_text.strip():
                documents.append({"text": combined_text, "page": page_num})

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
    return files
