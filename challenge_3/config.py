"""Configuration file"""
import os, binascii

class ConfigBase():
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bookameal'

class ConfigDevelopment(ConfigBase):
    """For development. Inherit from ConfigBase and overide some values"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/develop_bookameal'

class ConfigProduction(ConfigBase):
    """For Production. Inherit from Configase and overide some values"""
    SECRET_KEY = binascii.hexlify(os.urandom(40))
