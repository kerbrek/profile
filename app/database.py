from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import config

engine: AsyncEngine = create_async_engine(
    config.DB_URL,
    pool_size=config.POOL_SIZE,
    max_overflow=config.MAX_OVERFLOW,
    pool_timeout=config.POOL_TIMEOUT,
    echo=config.ECHO,
)

async_session = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)
