#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :db.py
@Time      :2024/7/26 下午8:14
@Author    :XJC
@Description:
"""
import asyncio
import logging
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable,AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False)
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                class_=AsyncSession
            ),
            scopefunc=asyncio.current_task
        )

    @asynccontextmanager
    async def dk_async_session(self) -> AsyncIterator[AsyncSession]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
