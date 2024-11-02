"""
coding:utf-8
@Time:2022/8/4 22:45
@Author:XJC
@Description:
"""
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setting import settings


def _engine() -> Any:
    return create_engine(
        settings.sync_database_url,
        echo=settings.DB_ECHO_LOG, logging_name=settings.DB_LOGGING_NAME, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(bind=_engine(), expire_on_commit=False, future=True)
