import asyncio
from fastapi import FastAPI
import redis.asyncio as redis

from app.config import settings
from app.logging_config import get_logger

logger = get_logger("RedisManager")

class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client: redis.Redis = self._create_client()
        self.is_reconnecting = False 

    def _create_client(self):
        return redis.Redis(host=self.host, port=self.port, decode_responses=True)


    async def reconnect(self):
        if self.is_reconnecting:
            return 

        self.is_reconnecting = True

        try:
            self.client = self._create_client()
            await self.client.ping()
        except Exception as e:
            pass
        self.is_reconnecting = False

    async def check_connection(self):
        while True:
            try:
                if self.client:
                    await self.client.ping()
                else:
                    await self.reconnect()
                    await self.client.ping()
            except Exception as e:
                logger.error("🔴 Redis 연결 실패")
                await self.reconnect()
            finally:
                await asyncio.sleep(5)

    async def close(self):
        if self.client:
            await self.client.close()

