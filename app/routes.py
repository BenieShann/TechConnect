from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from . import db, mail
from .models import User, Job, Application
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm  # Add new forms for forgot/reset password

# Serializer for generating secure tokens
serializer = URLSafeTimedSerializer("SECRET_KEY")

def register_routes(app):

    # Home Page Route
    @app.route('/')
    def home():
        jobs = Job.query.all()  # Retrieve all jobs
        return render_template('home.html', jobs=jobs)

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
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
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

    # Apply for Job Route
    @app.route('/apply/<int:job_id>', methods=['POST'])
    @login_required
    def apply_for_job(job_id):
        job = Job.query.get_or_404(job_id)
        form = ApplicationForm()

        if form.validate_on_submit():
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
        return redirect(url_for('home'))

    # Route to Add Test Jobs to the Database
    @app.route('/add_jobs')
    def add_jobs():
        # Add 7 new jobs to showcase
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
            description="Build both client and server-side applications.",
            company_name="ALX Africa",
            location="Remote",
            job_type="Part-time",
            salary="KSh 70,000 - 90,000 per month",
            category="Software Development"
        )
        job4 = Job(
            title="Mobile App Developer",
            description="Design and develop mobile applications for Android and iOS.",
            company_name="TechConnect",
            location="Lagos, Nigeria",
            job_type="Contract",
            salary="KSh 60,000 - 80,000 per month",
            category="Mobile Development"
        )
        job5 = Job(
            title="Cybersecurity Analyst",
            description="Monitor, detect, and protect against cyber threats.",
            company_name="Holberton School",
            location="Remote",
            job_type="Full-time",
            salary="KSh 120,000 - 140,000 per month",
            category="Cybersecurity"
        )
        job6 = Job(
            title="DevOps Engineer",
            description="Automate infrastructure and deployment processes.",
            company_name="ALX Africa",
            location="Nairobi, Kenya",
            job_type="Full-time",
            salary="KSh 100,000 - 130,000 per month",
            category="DevOps"
        )
        job7 = Job(
            title="Cloud Solutions Architect",
            description="Design and implement cloud computing solutions.",
            company_name="TechConnect",
            location="Lagos, Nigeria",
            job_type="Full-time",
            salary="KSh 150,000 - 180,000 per month",
            category="Cloud Computing"
        )
        job8 = Job(
            title="UI/UX Designer",
            description="Design user interfaces and improve user experience.",
            company_name="TechCorp Solutions",
            location="Nairobi, Kenya",
            job_type="Contract",
            salary="KSh 50,000 - 70,000 per month",
            category="UI/UX Design"
        )

        # Add all jobs to the session
        db.session.add_all([job1, job2, job3, job4, job5, job6, job7, job8])
        db.session.commit()

        flash('Test jobs added successfully!', 'success')
        return redirect(url_for('home'))
