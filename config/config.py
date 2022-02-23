import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    TESTS_FOLDER = "tests"
    LOGGING_LEVEL = "DEBUG"
    HOST = "0.0.0.0"
    PORT = "1996"
    MONGO_URI = "mongodb://mongodb:27017/songs"

    def __init__(self):
        if os.getenv("PORT"):
            Config.PORT = os.getenv("PORT")
        if os.getenv("HOST"):
            Config.HOST = os.getenv("HOST")
        if os.getenv("LOGGING_LEVEL"):
            Config.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")
        if os.getenv("MONGO_URI"):
            Config.MONGO_URI = os.getenv("MONGO_URI")


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()

    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    def __init__(self):
        super().__init__()

    ENV = "test"
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
