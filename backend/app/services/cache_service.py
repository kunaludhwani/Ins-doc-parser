"""
Cache service for response caching
Implements TTL-based in-memory caching for expensive operations
"""
import hashlib
import json
from typing import Optional, Any
from cachetools import TTLCache
from app.config import settings


class CacheService:
    """
    In-memory cache with TTL support for API responses
    """

    def __init__(self):
        """Initialize cache with TTL and max size from config"""
        self.enabled = settings.CACHE_ENABLED
        self.cache = TTLCache(
            maxsize=settings.CACHE_MAX_SIZE,
            ttl=settings.CACHE_TTL_SECONDS
        ) if self.enabled else None

    def _generate_key(self, *args, **kwargs) -> str:
        """
        Generate cache key from function arguments

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Unique cache key (SHA256 hash)
        """
        # Create deterministic string representation
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self.enabled or self.cache is None:
            return None
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
        """
        if self.enabled and self.cache is not None:
            self.cache[key] = value

    def delete(self, key: str) -> None:
        """
        Delete value from cache

        Args:
            key: Cache key
        """
        if self.enabled and self.cache is not None:
            self.cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cache entries"""
        if self.enabled and self.cache is not None:
            self.cache.clear()

    def get_stats(self) -> dict:
        """
        Get cache statistics

        Returns:
            Dictionary with cache stats
        """
        if not self.enabled or self.cache is None:
            return {
                'enabled': False,
                'size': 0,
                'max_size': 0
            }

        return {
            'enabled': True,
            'size': len(self.cache),
            'max_size': self.cache.maxsize,
            'ttl': self.cache.ttl
        }


# Global cache instance
cache_service = CacheService()


def cache_key_from_text(text: str, operation: str = "default") -> str:
    """
    Generate cache key from text content

    Args:
        text: Text content to hash
        operation: Operation identifier (e.g., 'classification', 'explanation')

    Returns:
        Cache key
    """
    # Hash text content for consistent key generation
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    return f"{operation}:{text_hash}"
