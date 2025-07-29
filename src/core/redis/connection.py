from redis.asyncio import Redis, ConnectionPool

from src.core.settings.settings import settings

connection_pool = ConnectionPool(max_connections=4)
redis = Redis(
    host=settings.REDIS.HOST,
    port=settings.REDIS.PORT,
    db=settings.REDIS.DB_NUMBER,
    decode_responses=True,
    # connection_pool=connection_pool,
)
