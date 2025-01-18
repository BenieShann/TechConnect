from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from . import db, mail
from .models import User, Job, Application
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm 
import os, logging
from werkzeug.utils import secure_filename

# Serializer for generating secure tokens
serializer = URLSafeTimedSerializer('24f574e64621167ed13380cb37c44b09a93e79a65c5ff55b')

# Creating a Blueprint
routes = Blueprint('routes', __name__)




class Routes:
    def __init__(self, app):
        self.app = app
    # def register_routes(app):

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
            

        # @routes.route('/search', methods=['GET'])
        # def search():
        #     query = request.args.get('query', '').strip()  # Gets the search query
        #     if query:
        #         # Perform a search in your database
        #         # Filter job posts by title or description
        #         results = Job.query.filter(Job.title.ilike(f"%{query}%")).all()
        #     else:
        #         results = []  # No results if the query is empty

        #     return render_template('search_results.html', query=query, results=results)


        # # Search route
        # @routes.route('/search', methods=['GET'])
        # def search():
        #     query = request.args.get('query', '').strip()  # Gets the search query
        #     if query:
        #         # Perform a search in your database
        #         # Filter job posts by title or description
        #         results = Job.query.filter(Job.title.ilike(f"%{query}%")).all()
        #     else:
        #         results = []  # No results if the query is empty

        #     return render_template('search_results.html', query=query, results=results)

        # Login Route
        @app.route('/login', methods=['GET', 'POST'])
        def login():
            form = LoginForm()  # WTForms to handle the form
            if form.validate_on_submit():  # If the form is submitted and valid
                user = User.query.filter_by(username=form.username.data).first()
                if user and check_password_hash(user.password, form.password.data):
                    login_user(user)  # Log the user in
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Login unsuccessful. Please check your username and password.', 'danger')
            return render_template('login.html', form=form)

        # Register Route
        @app.route('/register', methods=['GET', 'POST'])
        def register():
            
            form = RegisterForm()
            if request.method ==  'POST': 
                # if form.validate_on_submit():
                # hashed_password = generate_password_hash(form.password.data, method='sha256')
                new_user = User(username=form.username.data, email=form.email.data, password=form.email.data)
                db.session.add(new_user)
                print(new_user)
                db.session.commit()
                flash('Your account has been created! You can now log in.', 'success')
                print("Registering 2.")
                return redirect(url_for('login'))
            

            print("Registering 1.")
            
            return render_template('register.html', form=form)
        


        # Forgot Password Route
        @app.route('/forgot_password', methods=['GET', 'POST'])
        def forgot_password():
            form = ForgotPasswordForm()
            if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                if user:
                    token = serializer.dumps(user.email, salt="password-reset-salt")
                    reset_url = url_for('reset_password', token=token, _external=True)
                    
                    # Sending the email
                    msg = Message("Password Reset Request", sender="no-reply@yourapp.com", recipients=[user.email])
                    msg.body = f"To reset your password, click the link: {reset_url}\n\nIf you did not request this, please ignore this email."
                    mail.send(msg)
                    flash('A password reset link has been sent to your email.', 'info')
                else:
                    flash('Email not found in the system.', 'danger')
            return render_template('forgot_password.html', form=form)

        # Reset Password Route
        @app.route('/reset_password/<token>', methods=['GET', 'POST'])
        def reset_password(token):
            try:
                email = serializer.loads(token, salt="password-reset-salt", max_age=3600)  # Token valid for 1 hour
            except (SignatureExpired, BadSignature):
                flash('The reset link is invalid or has expired.', 'danger')
                return redirect(url_for('forgot_password'))

            form = ResetPasswordForm()
            if form.validate_on_submit():
                user = User.query.filter_by(email=email).first()
                if user:
                    hashed_password = generate_password_hash(form.password.data, method='sha256')
                    user.password = hashed_password
                    db.session.commit()
                    flash('Your password has been reset successfully!', 'success')
                    return redirect(url_for('login'))
            return render_template('reset_password.html', form=form)

        # Logout Route
        @app.route('/logout')
        @login_required
        def logout():
            logout_user()
            flash('You have been logged out.', 'info')
            return redirect(url_for('home'))

        # Profile Page Route
        @app.route('/profile')
        @login_required
        def profile():
            applications = Application.query.filter_by(user_id=current_user.id).all()
            return render_template('profile.html', applications=applications)
            
        # Route to Add Test Jobs to the Database
        @app.route('/add_jobs')
        def add_jobs():
            try:
                # Adding 10 test jobs to showcase
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
                job3 = Job(
                    title="Full Stack Developer",
                    description="Develop both frontend and backend of web applications.",
                    company_name="Innovate Tech",
                    location="Mombasa, Kenya",
                    job_type="Full-time",
                    salary="KSh 90,000 - 110,000 per month",
                    category="Software Development"
                )
                job4 = Job(
                    title="UX/UI Designer",
                    description="Design user-friendly interfaces and improve user experiences.",
                    company_name="DesignLabs",
                    location="Nairobi, Kenya",
                    job_type="Part-time",
                    salary="KSh 60,000 - 80,000 per month",
                    category="Design"
                )
                job5 = Job(
                    title="Product Manager",
                    description="Manage the development and launch of new products.",
                    company_name="TechCorp Solutions",
                    location="Nairobi, Kenya",
                    job_type="Full-time",
                    salary="KSh 120,000 - 140,000 per month",
                    category="Product Management"
                )
                job6 = Job(
                    title="Business Analyst",
                    description="Analyze business needs and provide data-driven recommendations.",
                    company_name="Holberton School",
                    location="Mombasa, Kenya",
                    job_type="Full-time",
                    salary="KSh 70,000 - 90,000 per month",
                    category="Business Analysis"
                )
                job7 = Job(
                    title="DevOps Engineer",
                    description="Ensure smooth deployment and integration of applications.",
                    company_name="Tech Corp",
                    location="Nairobi, Kenya",
                    job_type="Full-time",
                    salary="KSh 100,000 - 130,000 per month",
                    category="DevOps"
                )
                job8 = Job(
                    title="Software Architect",
                    description="Design and develop software solutions for large-scale applications.",
                    company_name="Innovate Tech",
                    location="Mombasa, Kenya",
                    job_type="Full-time",
                    salary="KSh 130,000 - 160,000 per month",
                    category="Software Development"
                )
                job9 = Job(
                    title="QA Engineer",
                    description="Test software to ensure high-quality releases.",
                    company_name="DesignLabs",
                    location="Nairobi, Kenya",
                    job_type="Full-time",
                    salary="KSh 70,000 - 90,000 per month",
                    category="Quality Assurance"
                )
                job10 = Job(
                    title="Digital Marketing Specialist",
                    description="Manage online marketing campaigns and improve brand visibility.",
                    company_name="TechCorp Solutions",
                    location="Nairobi, Kenya",
                    job_type="Full-time",
                    salary="KSh 80,000 - 100,000 per month",
                    category="Marketing"
                )

                # Adding all jobs to the session
                db.session.add_all([job1, job2, job3, job4, job5, job6, job7, job8, job9, job10])
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
