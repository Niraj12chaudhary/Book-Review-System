# app/services/cache.py
import redis
import json
import logging
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            self.is_available = True
            logger.info("Redis connection established")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.redis_client = None
            self.is_available = False

    async def get(self, key: str) -> Optional[Any]:
        if not self.is_available:
            return None
        
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        if not self.is_available:
            return False
        
        try:
            self.redis_client.setex(key, ttl, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        if not self.is_available:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

cache_service = CacheService()