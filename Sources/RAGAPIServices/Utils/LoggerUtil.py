import logging

class LoggerUtil:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger("Utils.LoggerUtil")
            self._logger.setLevel(logging.DEBUG)

            # File handler
            file_handler = logging.FileHandler('RAGAPIServices.log')
            file_handler.setLevel(logging.DEBUG)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # Formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Avoid duplicate handlers if reinitialized
            if not self._logger.handlers:
                self._logger.addHandler(file_handler)
                self._logger.addHandler(console_handler)

    # Original convenience methods
    def log_info(self, message):
        self._logger.info(message)

    def log_warning(self, message):
        self._logger.warning(message)

    def log_error(self, message):
        self._logger.error(message)

    def log_debug(self, message):
        self._logger.debug(message)

    # Properties to use logger.info(), logger.error(), etc.
    @property
    def info(self):
        return self._logger.info

    @property
    def warning(self):
        return self._logger.warning

    @property
    def error(self):
        return self._logger.error

    @property
    def debug(self):
        return self._logger.debug
