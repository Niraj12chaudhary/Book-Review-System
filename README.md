Book Review Service
A robust FastAPI-based book review service with Redis caching, PostgreSQL persistence, and comprehensive testing.
Features

RESTful API with OpenAPI/Swagger documentation
Redis Caching with fallback strategy
PostgreSQL database with optimized indexing
Comprehensive Error Handling with graceful degradation
Unit & Integration Tests with >80% coverage
Performance Optimized with async operations

API Endpoints
MethodEndpointDescriptionGET/booksList all books (with caching)POST/booksCreate a new bookGET/books/{id}/reviewsGet reviews for a bookPOST/books/{id}/reviewsAdd review to a bookGET/docsOpenAPI documentationGET/healthHealth check endpoint
Tech Stack

Backend: Python 3.11, FastAPI
Database: PostgreSQL with SQLAlchemy ORM
Cache: Redis
Testing: Pytest
Documentation: OpenAPI/Swagger
Deployment: Docker & Docker Compose

Installation & Setup
Prerequisites

Python 3.11+
PostgreSQL
Redis
Docker (optional)

# Clone repository

git clone https://github.com/Niraj12chaudhary/Book-Review-System.git
cd book-review-service

# Create virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt

# Set environment variables

export DATABASE_URL="postgresql://user:password@localhost:5432/bookreviews"
export REDIS_URL="redis://localhost:6379"

# Run migrations

alembic upgrade head

# Start the server

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run all tests

pytest

# Run specific test file

pytest app/tests/books.py -v

# Run integration tests only

pytest app/tests/test_integration.py -v
