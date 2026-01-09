from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # allow cross-origin requests to our API during development
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    from .routes import bp
    app.register_blueprint(bp, url_prefix="/api")
    
    return app
