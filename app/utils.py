from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.config import async_engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()
logger = logging.getLogger(__name__)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
