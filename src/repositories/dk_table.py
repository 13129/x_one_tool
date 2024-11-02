#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :repositories.py
@Time      :2024/7/30 下午6:36
@Author    :XJC
@Description:
"""
from contextlib import AbstractContextManager
from typing import Callable, Type

from fastapi import status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.errors import DnsNotFoundError
from src.models import DkTableInfo, DkTableFieldInfo


class DkTableInfoRepository:
    """
    表管理crud
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_table_all(self):
        with self.session_factory() as session:
            query = select(DkTableInfo).options(joinedload(DkTableInfo.fields, innerjoin=True))
            result = paginate(session, query)
            return result.model_dump()
