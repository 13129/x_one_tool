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
from contextlib import asynccontextmanager,AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class Database:

    def __init__(self, db_url: str) -> None:
        self.async_engine = create_async_engine(db_url, echo=False)
        self.async_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.async_engine,
                class_=AsyncSession
            ),
            scopefunc=asyncio.current_task,
        )

    @asynccontextmanager
    async def dk_async_session(self) -> Callable[..., AbstractAsyncContextManager[Session]]:
        session = self.async_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
