from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://saleor:saleor@localhost:5432/fastapi"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

Base = declarative_base()
