"""
coding:utf-8
@Time:2022/7/31 21:10
@Author:XJC
@Description:
"""
from sqlalchemy.orm import Session
from src.base.db.db_session import SessionLocal
from src.base.db.db_session import _engine as sync_engine


def get_db() -> Session:
    """
    Dependency function that yields db sessions
    """
    with SessionLocal() as session:
        yield session


__all__ = [
    SessionLocal,
    get_db,
    sync_engine
]
