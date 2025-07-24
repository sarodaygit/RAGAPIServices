from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from Utils.LoggerUtil import LoggerUtil
from Stores.Weaviate.store import WeaviateConnection
import tempfile
import os

class WeaviateWriter:
    def __init__(self, prefix: str = "/pdr"):
        self.logger = LoggerUtil()
        self.weaviate_conn = WeaviateConnection()
        self.router = APIRouter(prefix=prefix)
        self.router.add_api_route("/store", self.store_documents, methods=["POST"], tags=["PDRWriter"])

    async def store_documents(
        self,
        class_name: str = Form(...),
        source_type: str = Form(...),  # "pdf", "txt", etc.
        batch_size: int = Form(10),
        file: UploadFile = File(...)
    ):
        """
        FastAPI route to receive a file and embed + store its vectors in Weaviate.
        """
        try:
            filename = file.filename
            suffix = os.path.splitext(filename)[-1].lower() or ".txt"

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            # Embedding and storing
            self.logger.info(f"📄 Received {filename}, storing to class '{class_name}' as {source_type}")
            self.weaviate_conn.embed_and_store(
                source_path_or_string=tmp_path,
                class_name=class_name,
                source_type=source_type,
                batch_size=batch_size
            )

            os.remove(tmp_path)

            return JSONResponse(
                content={"message": f"✅ Successfully embedded '{filename}' to Weaviate class '{class_name}'."}
            )

        except RuntimeError as re:
            raise HTTPException(status_code=400, detail=str(re))
        except Exception as e:
            self.logger.log_error(f"❌ Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while processing the file.")
