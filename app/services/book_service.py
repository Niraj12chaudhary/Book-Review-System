# app/services/book_service.py
from sqlalchemy.orm import Session
from sqlalchemy import desc
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
        cached_books = await cache_service.get(cache_key)
        if cached_books:
            logger.info("Books retrieved from cache")
            return cached_books
        
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
            
            # Cache the result
            await cache_service.set(cache_key, books_data, ttl=1800)  # 30 minutes
            logger.info("Books retrieved from database and cached")
            return books_data
            
        except Exception as e:
            logger.error(f"Database error while fetching books: {e}")
            raise

    @staticmethod
    async def create_book(db: Session, book_data: BookCreate) -> Book:
        try:
            db_book = Book(**book_data.dict())
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            
            # Invalidate cache
            await cache_service.delete("books:all")
            logger.info(f"Book created with ID: {db_book.id}")
            return db_book
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating book: {e}")
            raise

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def get_reviews_by_book_id(db: Session, book_id: int) -> List[Review]:
        return db.query(Review).filter(Review.book_id == book_id)\
                 .order_by(desc(Review.created_at)).all()

    @staticmethod
    async def create_review(db: Session, book_id: int, review_data: ReviewCreate) -> Review:
        try:
            db_review = Review(book_id=book_id, **review_data.dict())
            db.add(db_review)
            db.commit()
            db.refresh(db_review)
            
            logger.info(f"Review created for book {book_id}")
            return db_review
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating review: {e}")
            raise