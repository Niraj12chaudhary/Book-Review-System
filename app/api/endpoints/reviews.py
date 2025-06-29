# app/api/endpoints/reviews.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.book_service import BookService
from app.utils.exceptions import BookNotFoundException, DatabaseException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Remove the /books prefix from the routes since they should be mounted under /books
@router.get("/{book_id}/reviews", response_model=List[ReviewResponse])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all reviews for a specific book.
    
    Returns reviews sorted by creation date (newest first).
    """
    try:
        # Check if book exists
        book = BookService.get_book_by_id(db, book_id)
        if not book:
            raise BookNotFoundException(book_id)
        
        reviews = BookService.get_reviews_by_book_id(db, book_id)
        return reviews
    except BookNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving reviews for book {book_id}: {e}")
        raise DatabaseException("Failed to retrieve reviews")

@router.post("/{book_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_book_review(book_id: int, review_data: ReviewCreate, db: Session = Depends(get_db)):
    """
    Create a new review for a specific book.
    """
    try:
        # Check if book exists
        book = BookService.get_book_by_id(db, book_id)
        if not book:
            raise BookNotFoundException(book_id)
        
        review = await BookService.create_review(db, book_id, review_data)
        return review
    except BookNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error creating review for book {book_id}: {e}")
        raise DatabaseException("Failed to create review")