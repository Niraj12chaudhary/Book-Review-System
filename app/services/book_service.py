# app/services/book_service.py
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional
from app.models.book import Book
from app.models.review import Review
from app.schemas.book import BookCreate
from app.schemas.review import ReviewCreate
from app.services.cache import cache_service
import logging
from app.core.logger import logger


logger = logging.getLogger(__name__)

class BookService:
    
    @staticmethod
    async def get_all_books(db: Session) -> List[Book]:
        cache_key = "books:all"
        
        # Try to get from cache first
        try:
            cached_books = await cache_service.get(cache_key)
            if cached_books:
                logger.info("Books retrieved from cache")
                return cached_books
        except Exception as e:
            logger.warning(f"Cache retrieval failed: {e}")
        
        # Fallback to database
        try:
            books = db.query(Book).all()
            books_data = [
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "isbn": book.isbn,
                    "description": book.description,
                    "created_at": book.created_at,
                    "updated_at": book.updated_at
                } for book in books
            ]
            
            # Cache the result (with error handling)
            try:
                await cache_service.set(cache_key, books_data, ttl=1800)  # 30 minutes
                logger.info("Books retrieved from database and cached")
            except Exception as e:
                logger.warning(f"Caching failed: {e}")
                
            return books_data
            
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching books: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching books: {e}")
            raise

    @staticmethod
    async def create_book(db: Session, book_data: BookCreate) -> Book:
        try:
            # Use model_dump instead of deprecated dict()
            db_book = Book(**book_data.model_dump())
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            
            # Invalidate cache (with error handling)
            try:
                await cache_service.delete("books:all")
            except Exception as e:
                logger.warning(f"Cache invalidation failed: {e}")
                
            logger.info(f"Book created with ID: {db_book.id}")
            return db_book
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity constraint violation: {e}")
            # Re-raise as a more specific error for API layer
            if "UNIQUE constraint failed: books.isbn" in str(e):
                raise ValueError(f"Book with ISBN {book_data.isbn} already exists")
            raise ValueError(f"Data integrity error: {str(e)}")
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating book: {e}")
            raise ValueError(f"Database error: {str(e)}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating book: {e}")
            raise ValueError(f"Failed to create book: {str(e)}")

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
        try:
            return db.query(Book).filter(Book.id == book_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching book {book_id}: {e}")
            raise

    @staticmethod
    def get_reviews_by_book_id(db: Session, book_id: int) -> List[Review]:
        try:
            return db.query(Review).filter(Review.book_id == book_id)\
                     .order_by(desc(Review.created_at)).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching reviews for book {book_id}: {e}")
            raise

    @staticmethod
    async def create_review(db: Session, book_id: int, review_data: ReviewCreate) -> Review:
        try:
            # Use model_dump instead of deprecated dict()
            db_review = Review(book_id=book_id, **review_data.model_dump())
            db.add(db_review)
            db.commit()
            db.refresh(db_review)
            
            logger.info(f"Review created for book {book_id}")
            return db_review
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity constraint violation creating review: {e}")
            if "FOREIGN KEY constraint failed" in str(e):
                raise ValueError(f"Book with ID {book_id} does not exist")
            raise ValueError(f"Data integrity error: {str(e)}")
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating review: {e}")
            raise ValueError(f"Database error: {str(e)}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating review: {e}")
            raise ValueError(f"Failed to create review: {str(e)}")