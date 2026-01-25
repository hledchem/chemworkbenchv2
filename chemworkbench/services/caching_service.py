"""
services/caching_service.py

Unified caching layer for ChemWorkBench v2.

This service provides:
    - In-memory caching for expensive operations
    - A consistent API for future distributed cache backends
    - Optional TTL-based eviction
    - Safe serialization boundaries

The cache is intentionally simple for v2:
    - Key/value store
    - Optional expiration
    - No assumptions about data type

Future extensions:
    - Redis / Memcached backend
    - Disk-based cache
    - Cloud object cache (S3, Azure Blob, GCS)
"""

from __future__ import annotations
import time
from typing import Any, Dict, Optional

from chemworkbench.runtime.logging import get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)


class CacheEntry:
    """
    Internal structure for cached values.
    """
    def __init__(self, value: Any, ttl: Optional[float] = None):
        self.value = value
        self.timestamp = time.time()
        self.ttl = ttl

    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.timestamp) > self.ttl


class CachingService:
    """
    High-level caching service.

    Responsibilities:
        - Provide a simple in-memory cache
        - Support TTL-based expiration
        - Offer a clean API for pipeline, processors, and services
    """

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a cached value if present and not expired.
        """
        entry = self._cache.get(key)

        if entry is None:
            logger.debug(f"Cache miss: {key}")
            return None

        if entry.is_expired():
            logger.debug(f"Cache expired: {key}")
            del self._cache[key]
            return None

        logger.debug(f"Cache hit: {key}")
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """
        Store a value in the cache with optional TTL.
        """
        self._cache[key] = CacheEntry(value, ttl)
        logger.debug(f"Cache set: {key} (ttl={ttl})")

    def delete(self, key: str):
        """
        Remove a key from the cache.
        """
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache delete: {key}")

    def clear(self):
        """
        Clear the entire cache.
        """
        self._cache.clear()
        logger.info("Cache cleared")

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def memoize(self, key: str, ttl: Optional[float], fn, *args, **kwargs):
        """
        Memoize the result of a function call.

        Example:
            result = cache.memoize("uvvis_baseline", 60, compute_baseline, data)
        """
        cached = self.get(key)
        if cached is not None:
            return cached

        try:
            result = fn(*args, **kwargs)
        except Exception as exc:
            raise PipelineError(f"Memoized function failed: {exc}") from exc

        self.set(key, result, ttl)
        return result
        

# ----------------------------------------------------------------------
# Singleton instance
# ----------------------------------------------------------------------

caching_service = CachingService()
