from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from . import db, mail
from .models import User, Job, Application
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm  # Add new forms for forgot/reset password
import os
from werkzeug.utils import secure_filename

# Serializer for generating secure tokens
serializer = URLSafeTimedSerializer("SECRET_KEY")

def register_routes(app):

    # Home Page Route
    @app.route('/')
    def home():
        try:
            jobs = Job.query.all()  # Retrieve all jobs from the database
            if not jobs:
                flash("No jobs found! Try adding some test jobs.", "warning")
            return render_template('home.html', jobs=jobs)
        except Exception as e:
            flash(f"Error retrieving jobs: {e}", "danger")
            return render_template('home.html', jobs=[])

    # Route to Add Test Jobs to the Database
    @app.route('/add_jobs')
    def add_jobs():
        try:
            # Add 8 test jobs to showcase
            job1 = Job(
                title="Software Engineer",
                description="Develop and maintain software solutions.",
                company_name="TechCorp Solutions",
                location="Nairobi, Kenya",
                job_type="Full-time",
                salary="KSh 100,000 - 120,000 per month",
                category="Software Development"
            )
            job2 = Job(
                title="Data Scientist",
                description="Analyze large datasets to extract insights and predictions.",
                company_name="Holberton School",
                location="Nairobi, Kenya",
                job_type="Full-time",
                salary="KSh 80,000 - 100,000 per month",
                category="Data Science"
            )
            # Add more jobs as needed (you already listed 8)

            # Add all jobs to the session
            db.session.add_all([job1, job2])
            db.session.commit()

            flash('Test jobs added successfully!', 'success')
        except Exception as e:
            flash(f"Error adding jobs: {e}", "danger")

        return redirect(url_for('home'))

    # Apply for Job Route
    @app.route('/apply/<int:job_id>', methods=['POST'])
    @login_required
    def apply_for_job(job_id):
        job = Job.query.get_or_404(job_id)
        form = ApplicationForm()

        if form.validate_on_submit():
            try:
                # Save the uploaded resume
                resume = form.resume.data
                resume_filename = secure_filename(resume.filename)
                resume_path = os.path.join('uploads', resume_filename)
                resume.save(resume_path)

                # Create a new application
                application = Application(
                    user_id=current_user.id,
                    job_id=job.id,
                    cover_letter=form.cover_letter.data,
                    resume_path=resume_path
                )
                db.session.add(application)
                db.session.commit()

                flash(f'You have successfully applied for the job: {job.title}', 'success')
            except Exception as e:
                flash(f"Error submitting application: {e}", "danger")
        return redirect(url_for('home'))
