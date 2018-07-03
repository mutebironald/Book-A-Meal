import os
import binascii


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = binascii.hexlify(os.urandom(24))


class DevelopmentConfig(Config):
    """Configurations for Development."""
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/bookameal'
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/bookameal'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
