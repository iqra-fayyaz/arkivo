# Arkivo 🎓📁

**Arkivo** is a Django-based web application designed to manage university project submissions, supervisor feedback, plagiarism detection, and grading. It features secure role-based access for students, supervisors, and admins.

---

## Features

### 🧑‍🎓 Student
- Register/login and select role during signup
- Submit projects with SRS, SDD, UI/UX documents, and GitHub repo link
- View plagiarism score (mocked Turnitin integration)
- Access grades, supervisor feedback, and submission status
- Interact with supervisor through comments

### 🧑‍🏫 Supervisor
- View student submissions
- Provide feedback and grades
- Respond to student comments via the frontend

### 🛠️ Admin
- View all projects
- Edit or delete any submission
- Access all user/project data

---

## 💡 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3 (Custom styling via `index.css`), javascript
- **Auth**: Django built-in + custom user model
- **Database**: SQLite (default)
- **Plagiarism Detection**: Mock Turnitin API

## 📌 Notes
- This project uses a mock plagiarism score generator until a real Turnitin API is integrated.
- Roles (Student, Supervisor, Admin) are selected during signup and affect dashboard access.
- Project files must be uploaded in .pdf or .docx format.
