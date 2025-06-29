# app/api/endpoints/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.core.database import get_db
from app.schemas.book import BookCreate, BookResponse
from app.services.book_service import BookService
from app.utils.exceptions import DatabaseException
import logging
from app.core.logger import logger


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
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving books: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while retrieving books"
        )
    except Exception as e:
        logger.error(f"Unexpected error retrieving books: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve books"
        )

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book.
    
    This endpoint creates a new book and invalidates the books cache.
    """
    try:
        book = await BookService.create_book(db, book_data)
        return book
    except ValueError as e:
        # Handle specific validation/business logic errors
        error_msg = str(e)
        logger.error(f"Validation error creating book: {error_msg}")
        
        if "already exists" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
    except SQLAlchemyError as e:
        logger.error(f"Database error creating book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating book"
        )
    except Exception as e:
        logger.error(f"Unexpected error creating book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create book"
        )