from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize database and login manager instances
db = SQLAlchemy()
login_manager = LoginManager()

# Define the application factory function
def create_app():
    # Create the Flask app instance
    app = Flask(__name__)
    
    # Application configuration
    app.config['SECRET_KEY'] = '24f574e64621167ed13380cb37c44b09a93e79a65c5ff55b'  # Secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tech_connect.db'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warnings for SQLAlchemy
    
    # Initialize database and login manager with the app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Set up the login view for unauthenticated users
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'  # Customize the flash message category
    
    # Create the database tables
    with app.app_context():
        from . import routes  # Import routes within the app context
        db.create_all()

    return app

