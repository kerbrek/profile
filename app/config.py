import multiprocessing
import os

WORKERS_DEFAULT = multiprocessing.cpu_count()
WORKERS = int(os.environ.get("WORKERS", WORKERS_DEFAULT))

DB_URL_TEMPLATE = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
DB_URL = DB_URL_TEMPLATE.format(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"],
    database=os.environ["POSTGRES_DB"],
)

DB_MAX_CONNECTIONS = int(os.environ.get("DB_MAX_CONNECTIONS", 100))
POOL_SIZE_DEFAULT = DB_MAX_CONNECTIONS // WORKERS

POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", POOL_SIZE_DEFAULT))
MAX_OVERFLOW = int(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", 0))
POOL_TIMEOUT = float(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", 30.0))
ECHO = bool(int(os.environ.get("DEBUG", 0)))
