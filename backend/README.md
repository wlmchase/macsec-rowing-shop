# CS6417 Rowing Shop Backend

This is the backend service for the CS6417 Rowing Shop application built with FastAPI.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
- Create a PostgreSQL database named `cs6417-rowing-shop`
- Update database credentials in `app/core/database.py` if needed
- Run migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## API Endpoints

The API includes the following main endpoints:

- `/api/auth` - Authentication endpoints
- `/api/users` - User management
- `/api/products` - Product management
- `/api/orders` - Order management
- `/api/contact` - Contact form submissions

## Development

To create new database migrations:
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```
