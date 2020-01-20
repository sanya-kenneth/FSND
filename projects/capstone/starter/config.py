import os

dialect = 'postgres://'


class BaseConfig:
    """
    Default configuration. Details from this configuration
    class are shared across all environments
    """
    DEBUG = False
    TESTING = False
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = dialect + 'postgres:psql@localhost:5432/capstone'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """
    Development configuraion. Loads development configuration data
    when the app is in the development environment
    """
    DEBUG = True
    TESTING = False
    ENV = "Development"
    SQLALCHEMY_DATABASE_URI = dialect + 'postgres:psql@localhost:5432/capstone'


class TestingConfig(BaseConfig):
    """
    Testing configuraion. Loads Test configuration data
    when the app is in the Test environment
    """
    DEBUG = True
    TESTING = True
    ENV = "Testing"
    db = 'test_capstone'
    SQLALCHEMY_DATABASE_URI = dialect + 'postgres:psql@localhost:5432/' + db


class ProductionConfig(BaseConfig):
    """
    Production configuraion. Loads Production configuration data
    when the app is in the Production environment
    """
    DEBUG = True
    TESTING = False
    ENV = "Production"
    SQLALCHEMY_DATABASE_URI = os.getenv('production_db')


app_config = {
    "Development": DevelopmentConfig,
    "Testing": TestingConfig,
    "Production": ProductionConfig
}
