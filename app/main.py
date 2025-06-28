from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import books, reviews
from app.core.config import settings
from app.services.cache import cache_service  # 👈 Import CacheService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="A simple book review service with caching support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(reviews.router, tags=["reviews"])


@app.on_event("startup")
async def startup_event():
    """
    Runs when the app starts. Checks if Redis cache is connected.
    """
    if cache_service.is_available:
        logger.info(" Redis connection established successfully.")
    else:
        logger.warning(" Redis connection failed. Cache will not work.")


@app.get("/")
def read_root():
    return {"message": "Welcome to Book Review Service", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.app_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
