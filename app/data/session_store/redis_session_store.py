""" Redis implementation of SessionStore """

import aioredis
import pickle
import asyncio
from app.entities.session import Session
from .session_store import SessionStore, SessionNotFound
from ...config.config import REDIS_URL, config, REDIS_EXPIRATION


def get_lock_name(session_id: str):
    return f'lock-{session_id}'


class RedisSessionStore(SessionStore):

    async def init_pool(self):
        self.__redis = await aioredis.create_redis_pool(config[REDIS_URL])

    async def save(self, session: Session) -> None:
        pickled_object = pickle.dumps(session)
        await self.__redis.set(session.id, pickled_object, expire=int(config[REDIS_EXPIRATION]))
        await self.__redis.delete(get_lock_name(session.id))

    async def get_one(self, session_id: str) -> Session:
        result = await self.__redis.get(session_id)
        if result is None:
            raise SessionNotFound

        return pickle.loads(result)

    async def get_one_and_lock(self, session_id: str) -> Session:
        acquired = 0

        while acquired == 0:
            acquired = await self.__redis.setnx(get_lock_name(session_id), 'true')
            if acquired == 0:
                await asyncio.sleep(0)

        await self.__redis.pexpire(get_lock_name(session_id), 100)

        return await self.get_one(session_id)


redis_session_store = RedisSessionStore()
