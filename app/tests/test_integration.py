# tests/test_integration.py
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

def test_cache_miss_integration(client: TestClient, sample_book):
    """Test the cache-miss path when Redis is unavailable."""
    
    with patch('app.services.cache.cache_service') as mock_cache:
        # Simulate cache miss/unavailability
        mock_cache.get.return_value = None
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
        mock_cache.get.assert_called()

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
    
    with patch('app.services.cache.cache_service') as mock_cache:
        # Simulate cache hit
        mock_cache.get.return_value = cached_books
        mock_cache.is_available = True
        
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert data == cached_books
        
        # Verify cache.get was called
        mock_cache.get.assert_called_with("books:all")