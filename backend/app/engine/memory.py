import time
from typing import Any, Dict


class MemoryStore:
    """
    A shared memory store for passing data between nodes during execution.
    For Phase 4, this is an in-memory dictionary.
    Later, this can be swapped out for a Redis-backed implementation if persistence is required.
    """

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def write(self, key: str, value: Any, ttl: int | None = None) -> None:
        """
        Write a value to the store.
        """
        expires_at = time.time() + ttl if ttl is not None else None
        self._store[key] = {"value": value, "expires_at": expires_at}

    def read(self, key: str, default: Any = None) -> Any:
        """
        Read a value from the store. Returns `default` if the key does not exist or has expired.
        """
        item = self._store.get(key)
        if not item:
            return default

        expires_at = item.get("expires_at")
        if expires_at is not None and time.time() > expires_at:
            # Key has expired
            del self._store[key]
            return default

        return item.get("value")

    def read_all(self) -> Dict[str, Any]:
        """
        Read all non-expired values from the store.
        """
        current_time = time.time()
        result = {}
        for key, item in list(self._store.items()):
            expires_at = item.get("expires_at")
            if expires_at is not None and current_time > expires_at:
                del self._store[key]
            else:
                result[key] = item.get("value")
        return result

    def clear(self) -> None:
        """
        Clear the entirely memory store.
        """
        self._store.clear()
