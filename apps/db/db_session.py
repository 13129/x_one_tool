"""
coding:utf-8
@Time:2022/8/4 22:45
@Author:XJC
@Description:
"""
from typing import Any

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from setting import settings


def _engine() -> Any:
    return create_async_engine(
        settings.async_database_url,
        echo=settings.DB_ECHO_LOG, logging_name=settings.DB_LOGGING_NAME, connect_args={"check_same_thread": False})


async_session = sessionmaker(bind=_engine(), class_=AsyncSession, expire_on_commit=False, future=True)
