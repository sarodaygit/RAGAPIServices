import weaviate
from Utils.ConfigParserUtil import ConfigParserUtil
from Utils.Embedders.PDFEmbedder import PDFEmbedder
import uuid
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

class WeaviateConnect:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None

        return cls._instance

    def __init__(self):
        if WeaviateConnect._instance.client is None:
            self.config = ConfigParserUtil()
            host = self.config.getValue("Weaviate", "Host")
            port = self.config.getValue("Weaviate", "Port")
            url = f"http://{host}:{port}"
            try:
                WeaviateConnect._instance.client = weaviate.Client(url)
                logging.info(f"✅ Connected to Weaviate at {url}")
            except Exception as e:
                logging.error(f"❌ Failed to connect to Weaviate: {e}")
                raise

    def get_client(self):
        """Return the Weaviate client instance."""
        if self.client is None:
            raise Exception("Weaviate client is not initialized.")
        return self.client

    @property
    def client(self):
        return WeaviateConnect._instance._client

    @client.setter
    def client(self, value):
        WeaviateConnect._instance._client = value


    def class_exists(self, class_name):
        """Check if a class already exists in the schema."""
        try:
            existing_classes = self.client.schema.get().get('classes', [])
            return any(cls['class'] == class_name for cls in existing_classes)
        except Exception as e:
            logging.error(f"❌ Failed to check class existence: {e}")
            return False

    def create_class(self, class_name, vectorizer="none"):
        """Create a Weaviate class schema if it doesn't already exist."""
        if not self.class_exists(class_name):
            schema = {
                "class": class_name,
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "page_number", "dataType": ["int"]},
                    {"name": "filename", "dataType": ["text"]}
                ],
                "vectorizer": vectorizer
            }
            try:
                self.client.schema.create_class(schema)
                logging.info(f"✅ Created Weaviate class: {class_name}")
            except Exception as e:
                logging.error(f"❌ Failed to create class {class_name}: {e}")

    # def store_documents(self, class_name, docs, filename):
    #     """Store a list of document objects into the specified class."""
    #     for doc in docs:
    #         try:
    #             self.client.data_object.create(
    #                 data_object={
    #                     "content": doc["text"],
    #                     "page_number": doc["page"],
    #                     "filename": filename
    #                 },
    #                 class_name=class_name,
    #                 vector=doc["vector"],
    #                 uuid=str(uuid.uuid4())
    #             )
    #             logging.info(f"📝 Stored page {doc['page']} of {filename} in Weaviate.")
    #         except Exception as e:
    #             logging.error(f"❌ Failed to store page {doc['page']} of {filename}: {e}")

    def store_documents(self, class_name, docs, filename, batch_size=10):
        """Store documents in batches for better performance."""
        if not docs:
            logging.warning(f"⚠️ No documents to store for {filename}")
            return

        try:
            with self.client.batch as batch:
                batch.batch_size = batch_size
                for doc in docs:
                    batch.add_data_object(
                        data_object={
                            "content": doc["text"],
                            "page_number": doc["page"],
                            "filename": filename
                        },
                        class_name=class_name,
                        uuid=str(uuid.uuid4()),
                        vector=doc["vector"]
                    )
                    logging.info(f"📝 Queued page {doc['page']} of {filename}")
            logging.info(f"✅ Finished storing {len(docs)} pages from {filename} in batches")
        except Exception as e:
            logging.error(f"❌ Failed to store documents in batch for {filename}: {e}")


    def test_connection(self):
        """Check if the client is connected to Weaviate and ready."""
        try:
            return self.client.is_ready()
        except Exception as e:
            logging.warning(f"⚠️ Weaviate connection test failed: {e}")
            return False

    def embed_pdf_and_store(self, pdf_path, class_name):
        """
        Embed the content of a PDF file and store the vectors in Weaviate.
        """
        embedder = PDFEmbedder()
        filename = pdf_path.split("/")[-1]
        try:
            logging.info(f"📄 Embedding and storing: {filename}")
            embeddings = embedder.embed_file(pdf_path)
            self.store_documents(class_name, embeddings, filename)
        except Exception as e:
            logging.error(f"❌ Failed to embed and store {filename}: {e}")
