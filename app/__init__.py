from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail, Message

# Initialize database, mail, login manager instances
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

# Defines the application factory function
def create_app(config_name='development'):
    # Create the Flask app instance
    app = Flask(__name__)
    
    # Application configuration
    app.config['SECRET_KEY'] = '24f574e64621167ed13380cb37c44b09a93e79a65c5ff55b'  # Secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tech_connect.db'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress app.config['MAIL_DEFAULT_SENDER'] = 'noreply@techconnect.com' warnings for SQLAlchemy
    
    # Add Mailtrap SMTP credentials for testing email functionality
    app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '6756e0883a6b62'
    app.config['MAIL_PASSWORD'] = '345c80f0a4dc27'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@techconnect.com' 

    
    # Initialize database, mail, login manager with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from .routes import register_routes
    register_routes(app)

    # Set up the login view for unauthenticated users
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'  # Customize the flash message category

    # Add the user_loader function here
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fixed the typo here (from 'ser_id' to 'user_id')
    
    # Create the database tables
    with app.app_context():
        db.create_all()

    return app
