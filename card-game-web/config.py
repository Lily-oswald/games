import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24).hex())
    FLASK_ENV = 'development'
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    # Add any other configuration settings as needed

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    DEBUG = False
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    
# Export the active configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get the active configuration based on FLASK_ENV."""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])