"""
coding:utf-8
@Time:2022/7/31 21:10
@Author:XJC
@Description:
"""
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.db_session import async_session
from apps.db.db_session import _engine as async_engine


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as ay_session:
        yield ay_session
        await ay_session.commit()


__all__ = [
    "async_session",
    "get_db",
    "async_engine"
]
