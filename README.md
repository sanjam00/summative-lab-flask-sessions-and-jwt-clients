# Journal Entries API

## Description

Journal Entries API is a Flask backend application that allows users to create and manage personal journal entries securely using JWT authentication.

Users can:
- Sign up for an account
- Log in securely
- Create journal entries
- View their own journal entries
- Update existing journal entries
- Delete journal entries

The API uses JWT authentication to protect routes and ensure users can only access their own data.

---

## Technologies Used

- Python
- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-Cors
- Flask-Marshmallow
- SQLite

---

## Installation Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Install Dependencies:

If using pipenv:
```bash
pipenv install
pipenv shell
```

Or with pip:
```bash
pip install -r requirements.txt
```

### Database Setup:

Cd into server, initialize migrations (first time only), migrate and seed the database:
``` bash
cd server
flask db init
flask db migrate -m "initial migration"
flask db upgrade
python seed.py
```

---

## Run Instructions

### Start the Flask server:

``` bash
python app.py
```

The backend will run on:
http://localhost:5555

---

## Authentication

This API uses JWT authentication.
Protected routes require an Authorizaiton header:
```
Authorization: Bearer <token>
```

A token is returned after successful login or signup.

---

## API/Auth Endpoints and Overview

---

### POST /signup

**Description:** Creates a new user account and returns a JWT token.
**Request Body:**
```json
{
  "username": "testuser",
  "password": "password123",
  "password_confirmation": "password123"
}
```
**Response:**
```json
{
  "token": "<jwt-token>",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
```

---

### POST /login

**Description:** Authenticates an existing user and returns a JWT token.
**Request Body:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```
**Response:**
```json
{
  "token": "<jwt-token>",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
```

---

### GET /me

**Description:** Returns the currently authenticated user.
**Headers:**
```
Authorization: Bearer <token>
```
**Response:**
```json
{
  "id": 1,
  "username": "testuser"
}
```

---

## Journal Entry Endpoints and Overview

All journal entry routes require JWT authentication.

---

### GET /entries

**Description:** Returns a paginated list of the authenticated user's journal entries.
**Query Parameters:**
page... page number
per_page... number of entries per page

**Example:**
```
GET /entries?page=1&per_page=5
```

**Response:**
```json
{
  "entries": [],
  "total_pages": 1,
  "current_page": 1,
  "has_next": false,
  "has_prev": false
}
```

---

### GET /entries/<id>

**Description:** Returns a single journal entry belonging to the authenticated user.

---

### POST /entries

**Description:** Creates a new journal entry.
**Request Body:**
```json
{
  "title": "My Journal Entry",
  "body": "Today was a good day."
}
```

---

### PATCH /entries/<id>

**Description:** Updates a journal entry belonging to the authenticated user.
**Request Body:**
```json
{
  "title": "Updated Title",
  "body": "Updated journal text."
}
```

---

### DELETE /entries/<id>

**Description:** Deletes a journal entry belonging to the authenticated user.
**Response:**
```json
{
  "message": "204 Entry successfully deleted"
}
```
*Status Code:*
```
204 No Content
```

---

## Security Features
- Passwords are securely hashed using Flask-Bcrypt
- JWT authentication protects sensitive routes
- Users can only access their own journal entries
- Protected routes require valid JWT tokens

---

## Author

Sanaeya James

Created for the Flask Full Authentication Summative Lab.