"""
coding:utf-8
@Time:2022/7/31 21:10
@Author:XJC
@Description:
"""
# from contextlib import contextmanager
#
# from sqlalchemy.orm import Session, scoped_session, sessionmaker
#
# from .db_session import _engine as sync_engine
#
# SessionLocal = scoped_session(sessionmaker(bind=sync_engine(), autocommit=False, autoflush=False))
#
#
# @contextmanager
# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# __all__ = [
#     SessionLocal,
#     get_db,
#     sync_engine
# ]
