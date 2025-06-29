# tests/test_integration.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

def test_cache_miss_integration(client: TestClient, sample_book):
    """Test the cache-miss path when Redis is unavailable."""
    
    # Mock the cache service properly for async calls
    with patch('app.services.book_service.cache_service') as mock_cache:
        # Create async mock for get method
        mock_cache.get = AsyncMock(return_value=None)
        mock_cache.is_available = False
        
        # Create a book first  
        response = client.post("/books/", json=sample_book)
        assert response.status_code == 201
        
        # Test GET /books when cache is unavailable
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == sample_book["title"]
        
        # Verify cache.get was called (attempting to read from cache)
        mock_cache.get.assert_called_with("books:all")

def test_cache_hit_integration(client: TestClient, sample_book):
    """Test successful cache retrieval."""
    
    cached_books = [{
        "id": 1,
        "title": "Cached Book", 
        "author": "Cached Author",
        "isbn": "9876543210987",
        "description": "From cache",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": None
    }]
    
    # Mock the cache service in the service layer
    with patch('app.services.book_service.cache_service') as mock_cache:
        # Create async mock that returns cached data
        mock_cache.get = AsyncMock(return_value=cached_books)
        mock_cache.is_available = True
        
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert data == cached_books
        
        # Verify cache.get was called with correct key
        mock_cache.get.assert_called_with("books:all")

def test_cache_failure_fallback(client: TestClient, sample_book):
    """Test that app works even when cache service fails."""
    
    # Create a book first for database fallback
    response = client.post("/books/", json=sample_book)
    assert response.status_code == 201
    
    # Mock cache service to raise exception
    with patch('app.services.book_service.cache_service') as mock_cache:
        mock_cache.get = AsyncMock(side_effect=Exception("Cache service down"))
        mock_cache.is_available = False
        
        # Should still work by falling back to database
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == sample_book["title"]