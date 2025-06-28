# app/models/review.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reviewer_name = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    book = relationship("Book", back_populates="reviews")

# Add index for optimized fetching reviews by book
Index('idx_reviews_book_id_created_at', Review.book_id, Review.created_at.desc())