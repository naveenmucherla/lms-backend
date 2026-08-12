

# 📘 Learning Management System (LMS)

A full-stack **Learning Management System (LMS)** built with **Django REST Framework** and **React**, featuring **JWT-based authentication**, **role-based access control**, course management, progress tracking, and certificate generation.

---

## 🚀 Project Overview

The Learning Management System is designed to support three types of users:

* **Admin** – manages users, mentors, and courses
* **Mentor** – creates courses, chapters, and lessons
* **Student** – enrolls in courses, tracks progress, and downloads certificates

The system ensures secure access using **JSON Web Tokens (JWT)** and enforces permissions based on user roles.

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Tailwind CSS
* Axios
* React Router

### Backend

* Django
* Django REST Framework (DRF)
* Simple JWT (Authentication)

### Database

* SQLite (Development)

### Deployment

* Backend: **Render**
* Frontend: **Localhost (React)**

---

## ✨ Key Features

* JWT-based authentication (Access & Refresh tokens)
* Role-based access control (Admin / Mentor / Student)
* User registration and login
* Course, chapter, and lesson management
* Student progress tracking
* Certificate generation on course completion
* Secure REST APIs
* Deployed backend with live API access

---

## 📂 Project Structure

```
lms-backend/
│
├── accounts/        # User management, roles, authentication
├── courses/         # Courses, chapters, lessons
├── progress/        # Student progress tracking
├── certificates/    # Certificate generation
├── lms/             # Project settings and URLs
├── manage.py
└── requirements.txt
```

---

## 🔐 Authentication Flow

1. User logs in using username and password
2. Backend returns **JWT access & refresh tokens**
3. Tokens are stored in browser `localStorage`
4. Axios automatically attaches token to every API request
5. Backend validates token and role permissions

---

## ⚙️ Backend Setup (Local)

```bash
# Clone repository
git clone https://github.com/naveenfsku/lms-backend.git
cd lms-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

---

## ⚙️ Frontend Setup (Local)

```bash
# Install dependencies
npm install

# Start React app
npm run dev
```

> ⚠️ Update backend API URL in `src/api/api.js` before running frontend.

---

## 🌐 Live Deployment

### Backend (Live API)

```
https://lms-backend-v2g9.onrender.com/api/
```

> Backend APIs are deployed on **Render** and publicly accessible.

### Frontend

* Frontend is a **React client-side application**
* Executed locally due to deployment constraints
* Fully integrated with deployed backend APIs

---

## 🧪 Testing & Validation

Manual testing was performed to validate system functionality.

### Sample Test Cases

| Test Case     | Description              | Result |
| ------------- | ------------------------ | ------ |
| Login         | Valid credentials        | Pass   |
| Login         | Invalid credentials      | Pass   |
| JWT Auth      | Access protected APIs    | Pass   |
| Role Access   | Admin / Mentor / Student | Pass   |
| Course Access | Student view courses     | Pass   |
| Logout        | Token cleared            | Pass   |

---

## 📸 Screenshots Included

* Login page
* Role-based dashboards
* Course listing and details
* JWT tokens in localStorage
* Backend running on Render

---

## 🎓 Academic Use

This project is suitable for:

* Final-year academic submission
* Internship evaluation
* Resume project demonstration

---

## 👨‍💻 Author

Naveen Mucharla
B.Tech Student
Full Stack Developer (Django & React)

---

## 📜 License

This project is developed for **educational purposes**.

