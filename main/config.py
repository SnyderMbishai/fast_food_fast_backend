"""Application configuration."""

import os


class Config(object):
    """Base config class."""

    SECRET_KEY = os.environ['APP_SECRET_KEY']
    DEBUG = False


class TestingConfig(Config):
    """Configuration for testing environment."""

    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    """Configuration for development environment."""

    DEBUG = True

class ProductionConfig(Config):
    """Configuration for development environment."""

    DEBUG = False


configurations = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
