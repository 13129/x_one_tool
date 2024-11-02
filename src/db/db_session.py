"""
coding:utf-8
@Time:2022/8/4 22:45
@Author:XJC
@Description:
"""
from typing import Any

from sqlalchemy import create_engine, QueuePool
from sqlalchemy.orm import sessionmaker

from setting import settings


def _engine() -> Any:
    return create_engine(
        settings.sync_database_url,
        echo=settings.DB_ECHO_LOG,
        logging_name=settings.DB_LOGGING_NAME,
        poolclass=QueuePool,
        pool_size=30,
        pool_timeout=30,
        pool_recycle=7200,
    )
