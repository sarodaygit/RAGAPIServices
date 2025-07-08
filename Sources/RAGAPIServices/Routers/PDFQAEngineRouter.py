from fastapi import APIRouter, Query
from pydantic import BaseModel
from langchain_community.embeddings import OllamaEmbeddings
import weaviate
from typing import List, Dict, Any
from Utils.LoggerUtil import LoggerUtil


class PDFQAEngine:
    def __init__(self, model_name="nomic-embed-text", weaviate_url="http://localhost:8080"):
        self.embedder = OllamaEmbeddings(model=model_name)
        self.client = weaviate.Client(weaviate_url)
        self.logger = LoggerUtil()

    def ask(self, question: str, class_name="PDFPage", top_k=3) -> List[Dict[str, Any]]:
        try:
            vector = self.embedder.embed_query(question)
            result = self.client.query.get(class_name, ["content", "page_number", "filename"]) \
                .with_near_vector({"vector": vector}) \
                .with_limit(top_k) \
                .do()

            hits = result["data"]["Get"].get(class_name, [])
            return hits
        except Exception as e:
            self.logger.error(f"❌ PDFQAEngine failed: {e}")
            return []


class QueryRequest(BaseModel):
    question: str
    class_name: str = "PDFPage"
    top_k: int = 3


class PDFQARouter:
    def __init__(self, prefix: str = "/pdfqa"):
        self.router = APIRouter(prefix=prefix, tags=["PDFQA"])
        self.qa_engine = PDFQAEngine()

        self.router.add_api_route("/query", self.query_pdf, methods=["POST"])

    async def query_pdf(self, request: QueryRequest):
        results = self.qa_engine.ask(request.question, request.class_name, request.top_k)
        return {"results": results}
