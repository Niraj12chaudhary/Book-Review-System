# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def setup_database():
    """Create tables once per session"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(setup_database):
    """Clean database before each test"""
    # Clear all tables before each test
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_book():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "1234567890123",
        "description": "A test book description"
    }

@pytest.fixture
def sample_review():
    return {
        "reviewer_name": "Test Reviewer",
        "rating": 5,
        "comment": "Great book!"
    }

# Alternative: Unique data per test
@pytest.fixture
def unique_sample_book():
    import uuid
    return {
        "title": f"Test Book {uuid.uuid4().hex[:8]}",
        "author": "Test Author",
        "isbn": str(uuid.uuid4().int)[:13],
        "description": "A test book description"
    }