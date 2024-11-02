#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :db.py
@Time      :2024/7/26 下午8:14
@Author    :XJC
@Description:
"""
import logging
from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=False)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
