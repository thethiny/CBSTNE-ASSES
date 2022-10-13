from typing import Any
from datetime import datetime


class LRUCache():
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity should be a value")
        self.max_capacity = capacity
        self.cache = {}
        self.sorted_cache = []

    def get(self, key: Any):
        if key in self.cache:
            self.cache[key]["last_used"] = self.get_time()
            self.sort_cache()
            return self.cache[key]["value"]

        # Will return None on not found

    @property
    def cache_size(self) -> int:
        return len(self.cache)

    @property
    def cache_full(self) -> bool:
        return self.cache_size < self.max_capacity

    @classmethod
    def get_time(cls):
        return datetime.utcnow()

    def sort_cache(self) -> None:
        self.sorted_cache = sorted(self.sorted_cache, key=lambda a: self.cache[a]["last_used"]) # Last element is least used

    def set(self, key: Any, value: Any):
        data = {
            "last_used": self.get_time(),
            "value": value,
        }
        self.cache[key] = data
        self.sorted_cache.append(key)

    def insert(self, key: Any, value: Any):
        if not self.cache_full or key in self.cache: # Allow overwrite of keys
            self.set(key, value)
            return # Prevent the need for else

        least_used_key = self.sorted_cache.pop(0) # removes first element
        del self.cache[least_used_key]

        self.set(key, value)