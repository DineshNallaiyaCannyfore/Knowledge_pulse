import re
import json
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.core.constants import MODEL_NAME
from app.db.models import DocumentChunk
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


OLLAMA_CONFIG = {
    "model": "llama3:8b",
    "base_url": "http://localhost:11434",
    "temperature": 0.3,
}

llm = OllamaLLM(**OLLAMA_CONFIG)

embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)


def search_service(query, db):
    query_embedding = get_embedding(query)
    results = (
        db.execute(
            select(DocumentChunk)
            .options(joinedload(DocumentChunk.file))
            .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
            .limit(3)
        )
        .scalars()
        .all()
    )
    filtered_results = [
        {"content": r.content, "file": r.file.file_name}
        for r in results
        if r.file is not None
    ]
    llm_answer = send_to_llm(query, filtered_results)
    return llm_answer


def get_embedding(text: str):
    return embedding_model.embed_query(text)


def send_to_llm(query: str, search_results: list):
    context = "\n\n".join(
        [f"Source: {r['file']}\nContent: {r['content']}" for r in search_results]
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are an AI assistant for "Knowledge Pulse".

        Context:
        {context}

        Question:
        {question}

        Instructions:
            - Answer ONLY using the provided context.
            - If the answer is not found, respond exactly:
            "The information is not available in the provided documents."
            - Do NOT make up information.
            - Extract the correct source document name(s) from the context.
            - If multiple documents are used, return them as an array.
            - llm_answer must be a string and source_document must be an array of file names.
            
     

            STRICT OUTPUT FORMAT (JSON ONLY):
            {{
            "llm_answer": "...",
            "source_document": []
            }}

            Rules:
            - Return ONLY valid JSON
            - Do NOT add any explanation or extra text
            - Ensure JSON is properly formatted
            - source_document MUST be an array (even for single file)
        """
    )

    try:
        chain = prompt | llm
        response = chain.invoke({"context": context, "question": query})

        response_text = response if isinstance(response, str) else response.content
        response_text = response_text.strip()

        try:
            parsed_response = json.loads(clean_llm_response(response_text))
            return parsed_response
        except json.JSONDecodeError:
            return {
                "llm_answer": response_text,
                "source_document": extract_sources_from_context(search_results),
            }

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")
        return {
            "llm_answer": "Failed to generate answer. Please check Ollama is running.",
            "source_document": [],
        }


def clean_llm_response(content: str):
    cleaned = re.sub(r"```json|```", "", content).strip()
    return cleaned


def extract_sources_from_context(search_results: list):
    sources = [r["file"] for r in search_results if "file" in r]
    return list(set(sources))
