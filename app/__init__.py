from flask import Flask
from config import DevelopmentConfig
from .models import db
from flask_sqlalchemy import SQLAlchemy

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create database tables for our data models

    from .routes import configure_routes
    configure_routes(app)
    return app
