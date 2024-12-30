from . import db
from flask_login import UserMixin
from datetime import datetime

# User Model - This represents a user of the job board
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Optional: Explicitly defining table name

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(150), nullable=False, unique=True)  # Username for login
    password = db.Column(db.String(150), nullable=False)  # Hashed password for authentication
    email = db.Column(db.String(150), nullable=False, unique=True)  # User's email
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Account creation timestamp
    
    # Optional: You can add more fields like role (admin/user), profile_picture, etc.
    
    def __repr__(self):
        return f"<User {self.username}>"

# Job Model - This represents a job listing on the board
class Job(db.Model):
    __tablename__ = 'jobs'  # Optional: Explicitly defining table name

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each job
    title = db.Column(db.String(150), nullable=False)  # Job title
    description = db.Column(db.Text, nullable=False)  # Detailed job description
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the job was posted
    company_name = db.Column(db.String(150), nullable=False)  # Company offering the job
    location = db.Column(db.String(150), nullable=False)  # Job location (could be remote or specific city)
    job_type = db.Column(db.String(50), nullable=False)  # Type of job: Full-time, Part-time, etc.
    salary = db.Column(db.String(100), nullable=True)  # Optional: Salary or salary range
    status = db.Column(db.String(50), default='Open')  # Job status: Open, Closed, Filled, etc.
    
    def __repr__(self):
        return f"<Job {self.title} at {self.company_name}>"

# Application Model - This represents an application for a job
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the application
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User applying for the job
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)  # Job being applied for
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of when the application was submitted
    resume = db.Column(db.String(255), nullable=True)  # Optional: Path to the resume file
    cover_letter = db.Column(db.Text, nullable=True)  # Optional: Cover letter content

    user = db.relationship('User', backref=db.backref('applications', lazy=True))  # Relationship to User
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))  # Relationship to Job

    def __repr__(self):
        return f"<Application for {self.job.title} by {self.user.username}>"

