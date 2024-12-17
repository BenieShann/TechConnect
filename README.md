# *Tech Connect - Tech Job Board*

*Tech Connect* is a platform designed to bridge the gap between tech talent and companies looking to hire skilled professionals. It offers job seekers the ability to create detailed profiles, apply for jobs, and track their applications, while providing companies with a platform to post job openings and manage their hiring process.

---

## *Tech Stack*

- **Frontend**: JavaScript (React)
- **Backend**: JavaScript (Node.js with Express)
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Deployment**: Local hosting (for development purposes), planned deployment on cloud platforms (e.g., Heroku, AWS)

---

## *Features*

- **User Authentication**: Secure user registration and login for job seekers and employers.
- **User Profiles**: Job seekers can create and update profiles showcasing their skills, experience, and qualifications.
- **Company Job Postings**: Employers can post, edit, and delete job openings.
- **Job Search and Filtering**: Users can search and filter jobs based on keywords, location, skills, and more.
- **Application Tracking**: Job seekers can track the status of their applications, and employers can view applications for their job postings.
- **Responsive Design**: The platform is optimized for accessibility and a seamless experience across desktop, tablet, and mobile devices.

---

## *Milestones*

- [x] **User Authentication**: Implemented secure login and registration for both job seekers and employers.
- [x] **User Profile Creation**: Job seekers and employers can create and manage their profiles.
- [x] **Job Posting**: Employers can post and manage job listings.
- [x] **Application Tracking**: Both users and employers can track job applications and statuses.
- [x] **Responsive Design**: Designed to be mobile-friendly and accessible across devices.
- [ ] **Job Recommendations**: Personalized job recommendations based on the user’s profile (future enhancement).

---

## *Installation Instructions*

1. *Clone the repository*:
   ```bash
   git clone [(https://github.com/BenieShann/TechConnect)]
   cd TechConnect
   ```

2. *Install dependencies*:
   - For the frontend:
     ```bash
     cd client
     npm install
     ```
   - For the backend:
     ```bash
     cd server
     npm install
     ```

3. *Set up environment variables*:
   Create a `.env` file in the `server` directory with the following environment variables:
   ```bash
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET=your_jwt_secret
   PORT=5000
   ```

4. *Start the development servers*:
   - Frontend:
     ```bash
     cd client && npm start
     ```
   - Backend:
     ```bash
     cd server && npm run dev
     ```

---

## *Usage*

Once the servers are running, visit `http://localhost:3000` in your browser to access the application.

---

## **API Documentation**

### **Authentication Routes**

- **POST /api/auth/register**: Registers a new user.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "password": "passwordabc",
      "userType": "user",
      "name": "Benie Shann",
      "companyName": "ALX School",
      "skills": ["react", "node"]
    }
    ```
  - Response:
    ```json
    {
      "message": "Registration successful",
      "token": "jwt_token_here"
    }
    ```

- **POST /api/auth/login**: Authenticates a user and returns a JWT token.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "password": "passwordabc"
    }
    ```
  - Response:
    ```json
    {
      "message": "Login successful",
      "token": "jwt_token_here"
    }
    ```

### **Job Postings Routes**

- **GET /api/jobs**: Fetches all job postings.
  - Response:
    ```json
    [
      {
        "title": "Frontend Developer",
        "company": "ALX School",
        "description": "Building UI components using React",
        "location": "Nairobi",
        "skills": ["react", "css", "html"]
      }
    ]
    ```

- **POST /api/jobs/post**: Allows employers to post a new job.
  - Request Body:
    ```json
    {
      "title": "Backend Developer",
      "company": "Tech Solutions",
      "description": "Developing APIs using Node.js and MongoDB",
      "location": "Remote",
      "skills": ["node", "mongodb", "express"]
    }
    ```
  - Response:
    ```json
    {
      "message": "Job posted successfully"
    }
    ```

### **Job Applications Routes**

- **POST /api/applications**: Apply for a job.
  - Request Body:
    ```json
    {
      "jobId": "job_id_here",
      "userId": "user_id_here",
      "resume": "resume_url_here"
    }
    ```
  - Response:
    ```json
    {
      "message": "Application submitted successfully"
    }
    ```

---

## *Frontend Structure*

- *Home Page*: Displays available jobs with search and filter options.
- *Login/Signup Pages*: Allows users to log in or register.
- *User Profile*: Displays and manages user details and job application statuses.
- *Job Listings*: Allows users to view and apply for jobs.
- *Job Application*: Lets users apply for jobs and view application statuses.

---

## *Contributing*

We welcome contributions! To contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them
4. Submit a pull request for review

---

## *License*

This project is licensed under the MIT License.

---

## *Contact*

For any questions or feedback, please reach out to [Shann -0115957511].

---
