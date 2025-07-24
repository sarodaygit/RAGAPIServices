from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from Utils.Embedders.BaseEmbedder import BaseEmbedder

class PDFEmbedder(BaseEmbedder):
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        super().__init__()
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)

    def embed_file(self, file_path):
        reader = PdfReader(file_path)
        results = []

        for i, page in enumerate(reader.pages):
            raw_text = page.extract_text() or ""
            chunks = self.split_text(raw_text)

            if not chunks:
                continue

            vectors = self.get_embeddings(chunks)

            for chunk, vector in zip(chunks, vectors):
                results.append({
                    "text": chunk,
                    "vector": vector.tolist(),
                    "metadata": {
                        "page": i + 1,
                        "source": file_path
                    }
                })

        return results
