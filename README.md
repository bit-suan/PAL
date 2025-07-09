# 📘 PAL – Personal Academic Logger

PAL (Personal Academic Logger) is a comprehensive web application designed to help students and learners organize their academic journey through intelligent task management, activity tracking, and progress visualization.

---

## 📌 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Project Structure](#Project-Structure)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🔐 Secure user authentication using JWT
- 📝 Daily logs of academic activities
- 📋 Manage to-dos with due dates and status tracking
- 📊 Track productivity using analytics and streaks
- 🔔 Get reminders and motivational messages

---

## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework
- **Auth**: JSON Web Token (JWT)
- **Database**: SQLite (initial MVP)
- **Frontend**: HTML5 & CSS3, JavaScript (ES6+), Responsive Design
- **API**: RESTful
- **Documentation**: Swagger / Postman

---
## ️ Installation

### **Prerequisites**

- Python 3.8 or higher
- Git
- Virtual environment (recommended)


### **Setup Instructions**

1. **Clone the repository**

```shellscript
git clone https://github.com/bit-suan/PAL.git
cd PAL
```
2. **Create and activate virtual environment**

```shellscript
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```shellscript
pip install -r requirements.txt
```


4. **Apply database migrations**

```shellscript
python manage.py makemigrations
python manage.py migrate
```


5. **Create a superuser (optional)**

```shellscript
python manage.py createsuperuser
```


6. **Run the development server**

```shellscript
python manage.py runserver
```


7. **Access the application**

1. Open your browser and go to `http://127.0.0.1:8000`
2. Register a new account or login
---
## 🔐 Environment Variables

Create a `.env` file in the root directory and configure:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```
## Project Structure

```plaintext
PAL/
├── core/                      # Main application
│   ├── migrations/           # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── core/           # App-specific templates
│   │   ├── registration/   # Auth templates
│   │   └── base.html       # Base template
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── forms.py            # Django forms
│   ├── serializers.py      # DRF serializers
│   └── admin.py            # Admin configuration
├── pal_backend/             # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── README.md               # Project documentation
```

---

## API Documentation

### **Authentication Endpoints**
```plaintext
POST /login/          # User login
POST /signup/         # User registration
POST /logout/         # User logout
```
### **Dashboard Endpoints**
```plaintext
GET  /dashboard/      # Main dashboard view
GET  /profile/        # User profile settings
POST /profile/        # Update profile
```
### **Todo Management**
```plaintext
GET  /todos/          # List all todos
POST /todos/          # Create new todo
PUT  /todos/<id>/     # Update todo
DELETE /todos/<id>/   # Delete todo
POST /toggle-todo/<id>/ # Toggle todo status
```
### **Activity Logging**
```plaintext
GET  /logs/           # List activity logs
POST /logs/           # Create new log entry
GET  /logs/<id>/      # Get specific log
PUT  /logs/<id>/      # Update log entry
DELETE /logs/<id>/    # Delete log entry
```
### **Statistics**
```plaintext
GET  /stats/          # Get detailed statistics
GET  /api/stats/      # JSON statistics data
```
## 🧾 Data Models

### User

```json
{
  "id": int,
  "email": "user@example.com",
  "username": "username",
  "password": "hashed_password",
  "joined_at": "2025-05-10"
}
```

### Log

```json
{
  "id": int,
  "user": int,
  "date": "YYYY-MM-DD",
  "description": "Worked on assignments"
}
```

### Todo

```json
{
  "id": int,
  "user": int,
  "task": "Complete project report",
  "status": "pending",
  "due_date": "YYYY-MM-DD"
}
```

---

## 🤝 Contributing

1. Fork this repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍🎓 Developed With Passion by Students for Students


