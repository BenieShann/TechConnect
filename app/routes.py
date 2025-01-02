from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import User, Job, Application
from .forms import LoginForm, RegisterForm  #WTForms for form validation

# Home Page Route
@app.route('/')
def home():
    # Display jobs (or any other relevant data)
    jobs = Job.query.all()  # Example of retrieving all jobs
    return render_template('home.html', jobs=jobs)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  #WTForms to handle the form
    if form.validate_on_submit():  # If the form is submitted and valid
        user = User.query.filter_by(username=form.username.data).first()  # Retrieve the user by username
        if user and check_password_hash(user.password, form.password.data):  # Validate password
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to the homepage
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # WTForms to handle the form
    if form.validate_on_submit():  # If the form is submitted and valid
        # Hash the password before storing
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)  # Add the new user to the session
        db.session.commit()  # Commit the transaction to the database
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to the login page after registration
    return render_template('register.html', form=form)

# Logout Route
@app.route('/logout')
@login_required  # Ensures only logged-in users can access this route
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))  # Redirect to the homepage

# Profile Page (Optional) - Example of a route requiring login
@app.route('/profile')
@login_required  # Ensures that only logged-in users can access this route
def profile():
    # Display user's personal details and job applications
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', applications=applications)

# Apply for Job Route
@app.route('/apply/<int:job_id>', methods=['POST'])
@login_required  # Ensure only logged-in users can apply for jobs
def apply_for_job(job_id):
    job = Job.query.get_or_404(job_id)  # Retrieve the job by ID or 404 if not found
    # Optional: Handle application logic (e.g., save resume or cover letter)
    new_application = Application(user_id=current_user.id, job_id=job.id)
    db.session.add(new_application)  # Add the application to the session
    db.session.commit()  # Commit the transaction to the database
    flash(f'You have successfully applied for the job: {job.title}', 'success')
    return redirect(url_for('home'))  # Redirect to the homepage after applying


