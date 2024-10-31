from flask import Flask
from flask_restx import Api
from app.config import Config
from app.extensions import db
from app.routes import register_namespaces

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Swagger documentation
    api = Api(app, version='1.0', title='My API', description='API Documentation')
    
    # Register namespaces for Swagger
    register_namespaces(api)
    
    return app
