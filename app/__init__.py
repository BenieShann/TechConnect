from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize database and login manager instances
db = SQLAlchemy()
login_manager = LoginManager()

# Defines the application factory function
def create_app(config_name='development'):
    # Create the Flask app instance
    app = Flask(__name__)
    
    # Application configuration
    app.config['SECRET_KEY'] = '24f574e64621167ed13380cb37c44b09a93e79a65c5ff55b'  # Secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tech_connect.db'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warnings for SQLAlchemy
    
    # Initialize database and login manager with the app
    db.init_app(app)
    login_manager.init_app(app)

    from .routes import register_routes
    register_routes(app)

    # Set up the login view for unauthenticated users
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'  # Customize the flash message category

    # Add the user_loader function here
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(ser_id))  
    
    # Create the database tables
    with app.app_context():
        db.create_all()

    return app

