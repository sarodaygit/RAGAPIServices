from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any
from langchain.text_splitter import CharacterTextSplitter



class BaseEmbedder(ABC):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100, model_name: str = None):
        """
        Initialize the base embedder.

        :param chunk_size: Number of characters per chunk.
        :param chunk_overlap: Number of overlapping characters between chunks.
        :param model_name: Name of the underlying embedding model (for tracking/logging).
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model_name = model_name
        self.splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split_text(self, text: str) -> List[str]:
        """Split a long text into manageable chunks."""
        return self.splitter.split_text(text)

    def format_embeddings(
        self,
        chunks: List[str],
        vectors: List[List[float]],
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Return structured documents with text + vector + optional metadata.

        :param chunks: List of text chunks.
        :param vectors: Corresponding vector embeddings.
        :param metadata: Metadata to be attached to each chunk.
        :return: List of dicts, each with 'text', 'vector', and 'metadata'.
        """
        return [
            {
                "text": chunk,
                "vector": vector.tolist() if hasattr(vector, "tolist") else vector,
                "metadata": metadata or {}
            }
            for chunk, vector in zip(chunks, vectors)
        ]

    @abstractmethod
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Convert a list of texts into embeddings using the underlying model.

        :param texts: List of text chunks.
        :return: List of float embeddings.
        """
        pass

    @abstractmethod
    def embed_source(
        self,
        source: Union[str, Dict, List, Any],
        source_type: str = "text",
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Embed documents from various source types like PDF, TXT, JSON, raw text.

        :param source: The input source (e.g., file path, dict, raw string).
        :param source_type: Type of input: "pdf", "txt", "json", "text", "mongo", "mysql", etc.
        :param metadata: Additional metadata to store alongside each chunk.
        :return: List of dicts containing 'text', 'vector', and 'metadata'.
        """
        pass
