from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize database
    db.init_app(app)

    # Register Blueprints
    from .routes import register_routes
    register_routes(app)

    return app