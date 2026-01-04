import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #BASE CONFIGURATION
    SECRET_KEY = os.getenv("SECRET_KEY", 'dev_secret_key_change_in_production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class DevelompentConfig(Config):
    #Development configuration
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    #Production configuration
    DEBUG = False
    SQLALCHEMY_ECHO = False

config = {
    'development': DevelompentConfig,
    'production': ProductionConfig,
    'default': DevelompentConfig
}



