#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :repositories.py
@Time      :2024/7/30 下午6:36
@Author    :XJC
@Description:
"""
from contextlib import AbstractAsyncContextManager
from typing import Callable

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import DkTableInfo


class DkTableInfoRepository:
    """
    表管理crud
    """

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_all(self):
        async with self.session_factory() as session:
            query = select(DkTableInfo).options(joinedload(DkTableInfo.fields, innerjoin=True)).order_by(
                DkTableInfo.last_modify_time)
            result = await paginate(session, query)
            return result.model_dump()
