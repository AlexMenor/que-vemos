""" Redis implementation of SessionStore """

import aioredis
import pickle
from app.entities.session import Session
from .session_store import SessionStore, SessionNotFound
from ...config.config import REDIS_URL, config


class RedisSessionStore(SessionStore):
    async def init_pool(self):
        self.__redis = await aioredis.create_redis_pool(config[REDIS_URL])

    async def save(self, session: Session) -> None:
        pickled_object = pickle.dumps(session)
        await self.__redis.set(session.id, pickled_object)

    async def get_one(self, session_id: str) -> Session:
        result = await self.__redis.get(session_id)
        if result is None:
            raise SessionNotFound

        return pickle.loads(result)


redis_session_store = RedisSessionStore()
