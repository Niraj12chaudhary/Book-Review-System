# app/api/deps.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

def get_database() -> Session:
    return Depends(get_db)
