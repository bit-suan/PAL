# 📘 PAL – Personal Academic Logger

PAL (Personal Academic Logger) is a productivity-focused web and mobile application built to help university students log daily academic activities, manage to-do lists, set academic goals, and track productivity through visual streaks and graphs.

---

## 📌 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
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
- **Frontend**: React (web), React Native (mobile) *(optional for MVP)*
- **API**: RESTful
- **Documentation**: Swagger / Postman

---

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pal-academic-logger.git
   cd pal-academic-logger
````

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and configure:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 📡 API Endpoints (Examples)

### Auth

* `POST /api/auth/register` – Register a new user
* `POST /api/auth/login` – Login and receive JWT token

### Logs

* `POST /api/logs/` – Create a daily log
* `GET /api/logs/` – Get user logs
* `PUT /api/logs/<id>/` – Update a log
* `DELETE /api/logs/<id>/` – Delete a log

### Todos

* `POST /api/todos/` – Create a to-do item
* `GET /api/todos/` – List all to-dos
* `PUT /api/todos/<id>/` – Update a to-do item
* `DELETE /api/todos/<id>/` – Delete a to-do item

---

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

```

---

