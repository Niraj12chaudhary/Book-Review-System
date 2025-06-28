# app/schemas/book.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=10, max_length=13)
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True