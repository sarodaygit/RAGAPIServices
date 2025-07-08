from abc import ABC, abstractmethod
from langchain_community.embeddings import OllamaEmbeddings


class BaseEmbedder(ABC):
    def __init__(self, model_name="nomic-embed-text"):
        self.model = OllamaEmbeddings(model=model_name)

    @abstractmethod
    def embed_file(self, file_path):
        """Should return a list of dicts with 'page', 'text', and 'vector'."""
        pass
