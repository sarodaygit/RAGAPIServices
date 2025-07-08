import os
from configparser import ConfigParser


class ConfigParserUtil(ConfigParser):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.config = ConfigParser()
            cls._instance.loadConfig()
        return cls._instance

    def loadConfig(self):
        env = os.getenv("ENV", "dev").lower()  # default to 'dev'
        current_dir = os.path.dirname(os.path.abspath(__file__))

        filename = f"RAGAPIServices.{env}.conf"
        config_path = os.path.abspath(os.path.join(current_dir, '..', 'Conf', filename))

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"❌ Config file not found for ENV='{env}' at {config_path}")

        print(f"🔧 Loading config: {filename}")
        self.config_file_path = config_path
        self.config.read(config_path)

    def getValue(self, section, key):
        return self.config.get(section, key)
