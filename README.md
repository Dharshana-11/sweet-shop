# Sweet Shop Management System

A full-stack Sweet Shop Management System built using Django and Django REST Framework.
The project follows **Test-Driven Development (TDD)** and implements secure, role-based
APIs for managing sweets inventory.

---

## Features

### Authentication

- User registration
- JWT-based login
- Protected endpoints using access tokens

### Sweets Management

- Add, view, update sweets
- Search sweets by category
- Admin-only sweet deletion

### Inventory

- Purchase sweets (quantity decreases)
- Admin-only restocking

---

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- SimpleJWT
- SQLite (local development)

### Testing

- Django Test Framework
- REST Framework APITestCase

---

## Setup Instructions

### Clone the repository

```bash
git clone <your-repo-url>
cd sweet-shop
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create .env file

```bash
SECRET_KEY=your-secret-key
DEBUG=True
```

### Run migrations

```bash
python manage.py migrate
```

### Run tests

```bash
python manage.py test
```

### Run server

```bash
python manage.py runserver
```

### Testing

- All core features were developed using Red-Green-Refactor TDD.
- Tests validate authentication, authorization, inventory logic, and error handling.

## My AI Usage

I used AI tools as development assistants, not code replacement.

### Tools Used

- ChatGPT

### How I Used AI

- Clarifying Django REST Framework best practices
- Refactoring code for readability and safety
- Validating TDD flow and test design

### Reflection

AI helped me move faster and catch design issues early, but all business logic, structure, and decision were implemented and understood by me.

All AI-assisted commits are transparently marked using Git co-author trailers.

## License

This project is for evaluation and learning purposes.
