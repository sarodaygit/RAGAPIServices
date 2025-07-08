from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from Utils.LoggerUtil import LoggerUtil
from Stores.Weaviate.store import WeaviateConnect
from typing import Optional
from Utils.Embedders.PDFEmbedder import PDFEmbedder
import tempfile
import os
from fastapi.responses import JSONResponse

class PDRWriterRouter:
    def __init__(self, prefix: str):
        self.logger = LoggerUtil()
        self.weaviate_conn = WeaviateConnect()
        self.router = APIRouter(prefix=prefix)

        self.router.add_api_route("/store", self.store_documents, methods=["POST"], tags=["PDRWriter"])

    async def embed_pdf_and_store(self, pdf_path: str, class_name: str, batch_size: int = 10):
        """
        Embed the content of a PDF file and store the vectors in Weaviate.
        """
        embedder = PDFEmbedder()
        filename = os.path.basename(pdf_path)

        if not self.weaviate_conn.class_exists(class_name):
            raise RuntimeError(
                f"❌ Class '{class_name}' does not exist. You must call create_class('{class_name}') first."
            )

        try:
            self.logger.info(f"📄 Embedding and storing: {filename}")
            embeddings = embedder.embed_file(pdf_path)
            self.weaviate_conn.store_documents(class_name, embeddings, filename, batch_size=batch_size)
        except Exception as e:
            self.logger.log_error(f"❌ Failed to embed and store {filename}: {e}")
            raise

    async def store_documents(
        self,
        class_name: str = Form(...),
        file: UploadFile = File(...),
        batch_size: int = Form(10)
    ):
        """
        FastAPI route to receive a PDF and store its embeddings in Weaviate.
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            await self.embed_pdf_and_store(tmp_path, class_name, batch_size=batch_size)

            os.remove(tmp_path)

            return JSONResponse(
                content={"message": f"✅ Successfully stored '{file.filename}' in Weaviate class '{class_name}'."}
            )

        except RuntimeError as re:
            raise HTTPException(status_code=400, detail=str(re))
        except Exception as e:
            self.logger.log_error(f"❌ Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while processing the PDF.")
