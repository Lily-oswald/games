from app import create_app
from config import get_config
import os

# Create the Flask application
app = create_app()

# Configure the app using the config module
app_config = get_config()
app.config.from_object(app_config)

if __name__ == "__main__":
    # Get port from environment variable or use 5002 as default
    port = int(os.environ.get('PORT', 5002))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=app_config.DEBUG)