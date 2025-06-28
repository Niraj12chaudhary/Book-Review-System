# app/api/endpoints/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.book import BookCreate, BookResponse
from app.services.book_service import BookService
from app.utils.exceptions import DatabaseException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[BookResponse])
async def get_all_books(db: Session = Depends(get_db)):
    """
    Retrieve all books with caching support.
    
    This endpoint first attempts to retrieve books from Redis cache.
    If cache is unavailable or data is not found, it falls back to the database.
    """
    try:
        books = await BookService.get_all_books(db)
        return books
    except Exception as e:
        logger.error(f"Error retrieving books: {e}")
        raise DatabaseException("Failed to retrieve books")

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book.
    
    This endpoint creates a new book and invalidates the books cache.
    """
    try:
        book = await BookService.create_book(db, book_data)
        return book
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        raise DatabaseException("Failed to create book")