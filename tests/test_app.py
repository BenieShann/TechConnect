import unittest
from app import create_app, db
from app.models import User, Job, Application
from datetime import datetime

class AppTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """This method runs once before all tests."""
        cls.app = create_app('testing')  # Use the 'testing' configuration
        cls.client = cls.app.test_client()  # Get the Flask test client

    def setUp(self):
        """This method runs before each individual test."""
        with self.app.app_context():
            # Create all tables in the in-memory SQLite database
            db.create_all()

    def tearDown(self):
        """This method runs after each individual test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables after each test to ensure isolation

    def test_homepage(self):
        """Test the homepage route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # Expecting a 200 OK response

    def test_user_creation(self):
        """Test creating a user."""
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            
            # Fetch the user from the database and assert
            fetched_user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(fetched_user)
            self.assertEqual(fetched_user.username, 'testuser')

    def test_job_creation(self):
        """Test creating a job."""
        with self.app.app_context():
            job = Job(title='Software Developer', description='Develop cool stuff', company='Tech Co.')
            db.session.add(job)
            db.session.commit()
            
            # Fetch the job from the database and assert
            fetched_job = Job.query.filter_by(title='Software Developer').first()
            self.assertIsNotNone(fetched_job)
            self.assertEqual(fetched_job.title, 'Software Developer')
            self.assertEqual(fetched_job.company, 'Tech Co.')

    def test_application_creation(self):
        """Test creating an application."""
        with self.app.app_context():
            # First, create a user and job to associate the application with
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()

            job = Job(title='Software Developer', description='Develop cool stuff', company='Tech Co.')
            db.session.add(job)
            db.session.commit()

            # Create an application for the job by the user
            application = Application(user_id=user.id, job_id=job.id, application_date=datetime.now())
            db.session.add(application)
            db.session.commit()

            # Assert the application was added correctly
            self.assertEqual(Application.query.count(), 1)
            application_in_db = Application.query.first()
            self.assertEqual(application_in_db.user_id, user.id)
            self.assertEqual(application_in_db.job_id, job.id)

    def test_user_job_relationship(self):
        """Test the relationship between User and Job through Application."""
        with self.app.app_context():
            # Create user and job
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()

            job = Job(title='Software Developer', description='Develop cool stuff', company='Tech Co.')
            db.session.add(job)
            db.session.commit()

            # Create an application
            application = Application(user_id=user.id, job_id=job.id, application_date=datetime.now())
            db.session.add(application)
            db.session.commit()

            # Query the user's applications and check the related job
            user_applications = User.query.get(user.id).applications
            self.assertEqual(len(user_applications), 1)
            self.assertEqual(user_applications[0].job.title, 'Software Developer')

            # Query the job's applications and check the related user
            job_applications = Job.query.get(job.id).applications
            self.assertEqual(len(job_applications), 1)
            self.assertEqual(job_applications[0].user.username, 'testuser')

if __name__ == '__main__':
    unittest.main()

