from typing import Type
from Utils.Embedders.BaseEmbedder import BaseEmbedder
from Utils.Embedders.HuggingFaceEmbedder import HuggingFaceEmbedder
from Utils.Embedders.OllamaEmbedder import OllamaEmbedder
from Utils.ConfigParserUtil import ConfigParserUtil


class EmbedderFactory:
    """
    Dynamically creates the appropriate embedder instance based on configuration.
    """

    _registry = {
        "huggingface": HuggingFaceEmbedder,
        "ollama": OllamaEmbedder,
        # Extend here with other embedders like "openai": OpenAIEmbedder
    }

    @classmethod
    def create_embedder(cls) -> BaseEmbedder:
        config = ConfigParserUtil()
        
        model_type = config.getValue("Embedding", "model_type").lower()
        model_name = config.getValue("Embedding", "model_name")
        chunk_size = int(config.getValue("Embedding", "chunk_size"))
        chunk_overlap = int(config.getValue("Embedding", "chunk_overlap"))

        embedder_class: Type[BaseEmbedder] = cls._registry.get(model_type)

        if not embedder_class:
            raise ValueError(f"❌ Unsupported model_type: '{model_type}'. Available: {list(cls._registry.keys())}")

        print(f"📦 EmbedderFactory: Using {model_type} model '{model_name}' with chunk_size={chunk_size}, overlap={chunk_overlap}")
        return embedder_class(
            model_name=model_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
