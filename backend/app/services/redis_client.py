import json
import logging
from datetime import datetime, timezone

import redis.asyncio as redis

from app.config import get_settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Singleton asynchronous wrapper for Redis interactions."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance

    async def connect(self):
        """Initializes the connection pool if not already initialized."""
        if self.client is None:
            settings = get_settings()
            try:
                self.client = redis.from_url(settings.redis_url, decode_responses=True)
                # Test connection
                await self.client.ping()
                logger.info(f"Connected to Redis at {settings.redis_url}")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self.client = None

    async def save_run(self, workflow_id: str, run_data: dict) -> bool:
        """Saves a workflow run to the 'workflows:history' Hash map and updates sorted set."""
        if not self.client:
            await self.connect()
        if not self.client:
            return False

        try:
            timestamp = datetime.now(timezone.utc).isoformat()

            # Ensure the run_data contains the ID and timestamp
            data_to_store = {"id": workflow_id, "timestamp": timestamp, **run_data}

            payload = json.dumps(data_to_store)

            # ZADD uses the timestamp epoch to order lists chronologically
            epoch = datetime.now().timestamp()

            async with self.client.pipeline(transaction=True) as pipe:
                pipe.hset("workflows:history", workflow_id, payload)
                pipe.zadd("workflows:timeline", {workflow_id: epoch})
                await pipe.execute()

            return True
        except Exception as e:
            logger.error(f"Failed saving to Redis: {e}")
            return False

    async def get_all_runs(self, limit: int = 50) -> list[dict]:
        """Fetches latest workflows from timeline descending."""
        if not self.client:
            await self.connect()
        if not self.client:
            return []

        try:
            # Get latest ID's from timeline score
            latest_ids = await self.client.zrevrange("workflows:timeline", 0, limit - 1)
            if not latest_ids:
                return []

            # Fetch hashes
            raw_runs = await self.client.hmget("workflows:history", latest_ids)

            runs = []
            for raw in raw_runs:
                if raw:
                    runs.append(json.loads(raw))

            return runs
        except Exception as e:
            logger.error(f"Failed fetching runs from Redis: {e}")
            return []


redis_client = RedisClient()
