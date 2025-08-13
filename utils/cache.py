from typing import Optional, Any
from datetime import datetime, timedelta, timezone


class CachingUtility:
    def __init__(self):
        self.cache_key: dict = {}
        self.def_ttl = 3000

    async def get_value(self, key: str):
        if key not in self.cache_key:
            return None if key not in self.cache_key else self.cache_key[key]
        
        cache_entry = self.cache_key[key]
        if datetime.now(timezone.utc) > cache_entry['expires_at']:
            del self.cache_key[key]
            return None
        
        return cache_entry['value']

    async def delete_value(self, key: str) -> None:
        if key in self.cache_key:
            del self.cache_key[key]


    async def set_value(self, key: str, value: Any, time_to_live: Optional[int] = None) -> None:
        ttl = time_to_live or self.def_ttl
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
        self.cache_key[key] = {
            'value': value,
            'expires_at': expires_at
        }


    
    def _cleanup_expired(self):
        time_now = datetime.now(timezone.utc)
        expired_keys = [
            key for key, value in self.cache_key.items()
            if time_now > value['expires_at']
        ]
        for key in expired_keys:
            del self.cache_key[key]


cache = CachingUtility()