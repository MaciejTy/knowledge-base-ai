from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)

    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (route modules)
    from app.api.routes import documents
    app.register_blueprint(documents.bp)

    # Frontend route (DODAJ TO)
    @app.route('/')
    def index():
        return render_template('index.html')

    return app