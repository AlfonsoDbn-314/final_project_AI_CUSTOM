"""Implementacion CAG con Redis para persistencia real entre reinicios."""
import json
import redis


class ContextStoreRedis:
    def __init__(self, host="localhost", port=6379, db=0):
        self._client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def _key(self, user_id):
        return f"cag:context:{user_id}"

    def save(self, user_id, key, value):
        existing = self._client.get(self._key(user_id))
        data = json.loads(existing) if existing else {}
        data[key] = value
        self._client.set(self._key(user_id), json.dumps(data))
        return True

    def list_for_user(self, user_id):
        existing = self._client.get(self._key(user_id))
        if not existing:
            return []
        data = json.loads(existing)
        return [{"key": k, "value": v} for k, v in data.items()]