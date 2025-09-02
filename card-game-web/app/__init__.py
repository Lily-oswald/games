from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(24).hex()),
        SESSION_TYPE='filesystem'
    )
    
    with app.app_context():
        # Import and register blueprints
        from . import routes
        routes.init_app(app)

    return app