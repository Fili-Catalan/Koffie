from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import redis

# The following are extensions that must be bound to the Flask app so that every extension
# has access to app context and config.

# Initializing our database.
db = SQLAlchemy()

# Initializing migration tool.
migrate = Migrate()

# Initializing cryptographic string hasher.
bcrypt = Bcrypt()

redis_client = None

def create_app(database_url=None, redis_url=None):

    """
    
    The imports are in this class to prevent circular imports, due to interal imports to app.

    """

    # Sets environment variables at the application level, does not affect environment variables set
    # in Docker api-backend container.
    load_dotenv()

    global redis_client
    redis_client = redis.Redis.from_url(redis_url if redis_url is not None else os.environ.get('REDIS_URL'), decode_responses=True)

    # Creating our Flask app instance.
    app = Flask(__name__)

    # Load configs from environment variables file '.env'. In our case
    # we only want to load configs that are related to our app.
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url if database_url is not None else os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['REDIS_URL'] = redis_url if redis_url is not None else os.environ.get('REDIS_URL')

    # Bound to the app inside the factory.
    db.init_app(app)

    # Bind bcrypt extension to the Flask app.
    bcrypt.init_app(app)

    from app.models.user import User

    # Initialize migrate.init_app. Wire up the migration tool to the app.
    migrate.init_app(app,db)

    from app.api.v1.auth import auth_bp

    # Register authentication endpoints blueprint.
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    return app
