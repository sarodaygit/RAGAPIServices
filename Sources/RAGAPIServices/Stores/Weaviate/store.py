import weaviate
import uuid
import logging
from Utils.ConfigParserUtil import ConfigParserUtil
from Utils.Embedders.EmbedderFactory import EmbedderFactory

# Setup logging
logging.basicConfig(level=logging.INFO)

class WeaviateConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
        return cls._instance

    def __init__(self):
        if WeaviateConnection._instance.client is None:
            self.config = ConfigParserUtil()
            host = self.config.getValue("Weaviate", "Host")
            port = self.config.getValue("Weaviate", "Port")
            url = f"http://{host}:{port}"
            try:
                WeaviateConnection._instance.client = weaviate.Client(url)
                logging.info(f"✅ Connected to Weaviate at {url}")
            except Exception as e:
                logging.error(f"❌ Failed to connect to Weaviate: {e}")
                raise

    def get_client(self):
        if self.client is None:
            raise Exception("Weaviate client is not initialized.")
        return self.client

    @property
    def client(self):
        return WeaviateConnection._instance._client

    @client.setter
    def client(self, value):
        WeaviateConnection._instance._client = value

    def test_connection(self):
        try:
            return self.client.is_ready()
        except Exception as e:
            logging.warning(f"⚠️ Weaviate connection test failed: {e}")
            return False

    def class_exists(self, class_name):
        try:
            classes = self.client.schema.get().get('classes', [])
            return any(cls['class'] == class_name for cls in classes)
        except Exception as e:
            logging.error(f"❌ Failed to check class existence: {e}")
            return False

    def create_class(self, class_name, vectorizer="none"):
        if not self.class_exists(class_name):
            schema = {
                "class": class_name,
                "vectorizer": vectorizer,
                "properties": [
                    {"name": "text", "dataType": ["text"]},
                    {"name": "source", "dataType": ["text"]},
                    {"name": "page", "dataType": ["int"]}  # optional
                ]
            }
            try:
                self.client.schema.create_class(schema)
                logging.info(f"✅ Created Weaviate class: {class_name}")
            except Exception as e:
                logging.error(f"❌ Failed to create class {class_name}: {e}")

    def store_documents(self, class_name, docs: list, batch_size=10):
        if not docs:
            logging.warning("⚠️ No documents to store.")
            return

        try:
            with self.client.batch(batch_size=batch_size) as batch:
                for doc in docs:
                    batch.add_data_object(
                        data_object={**doc["metadata"], "text": doc["text"]},
                        class_name=class_name,
                        uuid=str(uuid.uuid4()),
                        vector=doc["vector"]
                    )
            logging.info(f"✅ Stored {len(docs)} vectors to class '{class_name}'")
        except Exception as e:
            logging.error(f"❌ Failed to store documents: {e}")

    def embed_and_store(
        self,
        source_path_or_string: str,
        class_name: str,
        source_type: str = "pdf",
        batch_size: int = 10
    ):
        try:
            embedder = EmbedderFactory.create_embedder()
            metadata = {"source": source_path_or_string.split("/")[-1]}

            logging.info(f"📄 Embedding from {source_type}: {source_path_or_string}")
            docs = embedder.embed_source(source_path_or_string, source_type=source_type, metadata=metadata)

            self.create_class(class_name)
            self.store_documents(class_name, docs, batch_size=batch_size)

        except Exception as e:
            logging.error(f"❌ Failed to embed and store: {e}")
