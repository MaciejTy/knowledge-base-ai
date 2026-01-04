from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Initialize extensions

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    #Application factory pattern
    app = Flask(__name__)

    #Load config
    from app.config import config
    app.config.from_object(config[config_name])

    #Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # #Register blueprints (API routes)
    # from app.api.routes import documents
    # app.register_blueprint(documents.bp)
    return app
