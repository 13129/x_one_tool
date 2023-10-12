"""
coding:utf-8
@Time:2022/8/4 22:45
@Author:XJC
@Description:
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from setting import settings

engine = create_async_engine(
    settings.async_database_url,
    echo=settings.DB_ECHO_LOG, connect_args={"check_same_thread": False}

)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, future=True)
