# app/schemas/review.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    reviewer_name: str = Field(..., min_length=1, max_length=255)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    created_at: datetime

    class Config:
        from_attributes = True