from pathlib import Path
from sentence_transformers import SentenceTransformer
from Utils.Embedders.BaseEmbedder import BaseEmbedder
from typing import List, Dict, Union
import json
from pypdf import PdfReader


class HuggingFaceEmbedder(BaseEmbedder):
    def __init__(self, model_name: str, chunk_size: int = 500, chunk_overlap: int = 100):
        """
        HuggingFace Embedder using sentence-transformers.
        """
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap, model_name=model_name)
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates dense vector embeddings from text chunks.
        """
        return self.model.encode(texts, convert_to_numpy=True)

    def embed_source(
        self,
        source: Union[str, Path],
        source_type: str = "text",
        metadata: Dict = None
    ) -> List[Dict]:
        """
        Extract, chunk, embed, and return list of dicts with 'text', 'vector', and 'metadata'.

        :param source: file path or raw string
        :param source_type: one of ["pdf", "txt", "json", "text"]
        :param metadata: optional metadata (e.g., source filename)
        :return: list of documents
        """
        metadata = metadata or {}

        if source_type == "pdf":
            content = self._extract_pdf(source)
        elif source_type == "txt":
            content = self._extract_txt(source)
        elif source_type == "json":
            content = self._extract_json(source)
        elif source_type == "text":
            content = str(source)
        else:
            raise ValueError(f"Unsupported source_type: {source_type}")

        chunks = self.split_text(content)
        vectors = self.get_embeddings(chunks)
        return self.format_embeddings(chunks, vectors, metadata=metadata)

    def _extract_pdf(self, file_path: Union[str, Path]) -> str:
        reader = PdfReader(str(file_path))
        return "\n".join([page.extract_text() or "" for page in reader.pages])

    def _extract_txt(self, file_path: Union[str, Path]) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _extract_json(self, file_path: Union[str, Path]) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
