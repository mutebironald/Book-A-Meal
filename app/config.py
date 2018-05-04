class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = 'rtnsjd'
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}