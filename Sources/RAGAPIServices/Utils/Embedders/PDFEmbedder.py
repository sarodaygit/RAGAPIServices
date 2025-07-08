from pypdf import PdfReader
from Utils.Embedders.BaseEmbedder import BaseEmbedder  # adjust import based on your folder structure

class PDFEmbedder(BaseEmbedder):
    def embed_file(self, file_path):
        reader = PdfReader(file_path)
        results = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                vector = self.model.embed_query(text)
                results.append({
                    "page": i + 1,
                    "text": text,
                    "vector": vector
                })
        return results
