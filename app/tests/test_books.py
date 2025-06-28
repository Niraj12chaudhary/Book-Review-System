# tests/test_books.py
import pytest
from fastapi.testclient import TestClient

def test_create_book(client: TestClient, sample_book):
    response = client.post("/books/", json=sample_book)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_book["title"]
    assert data["author"] == sample_book["author"]
    assert "id" in data

def test_get_all_books(client: TestClient, sample_book):
    # First create a book
    client.post("/books/", json=sample_book)
    
    # Then fetch all books
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == sample_book["title"]

def test_create_book_invalid_data(client: TestClient):
    invalid_book = {"title": "", "author": "Test Author"}  # Missing required fields
    response = client.post("/books/", json=invalid_book)
    assert response.status_code == 422

def test_get_book_reviews_not_found(client: TestClient):
    response = client.get("/books/99999/reviews")
    assert response.status_code == 404

def test_create_and_get_reviews(client: TestClient, sample_book, sample_review):
    # Create a book first
    book_response = client.post("/books/", json=sample_book)
    book_id = book_response.json()["id"]
    
    # Create a review
    review_response = client.post(f"/books/{book_id}/reviews", json=sample_review)
    assert review_response.status_code == 201
    review_data = review_response.json()
    assert review_data["rating"] == sample_review["rating"]
    assert review_data["book_id"] == book_id
    
    # Get reviews
    reviews_response = client.get(f"/books/{book_id}/reviews")
    assert reviews_response.status_code == 200
    reviews = reviews_response.json()
    assert len(reviews) == 1
    assert reviews[0]["rating"] == sample_review["rating"]