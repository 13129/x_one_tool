#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :repositories.py
@Time      :2024/7/30 下午6:36
@Author    :XJC
@Description:
"""
from contextlib import AbstractAsyncContextManager
from typing import Callable, Type, List

from fastapi import status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.errors import DnsNotFoundError
from src.models import DkCatalog


class DkCatalogRepository:
    """
    数据目录crud
    """

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_all(self, name) -> List[DkCatalog]:
         async with self.session_factory() as session:
            query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=False)).filter(
                DkCatalog.name_cn.like(f'%{name}%')).order_by(DkCatalog.order_no)
            result = await paginate(session, query)
            return result.model_dump()

    async def get_by_id(self, _id: str) -> DkCatalog:
        async with self.session_factory() as session:
            query = select(DkCatalog).where(DkCatalog.id == _id)
            result = await session.execute(query)
            result = result.scalar()
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, _id)
            return result

    async def delete_by_id(self, _id: str) -> Type[DkCatalog]:
        async with self.session_factory() as session:
            result = await session.get(DkCatalog, _id)
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, _id)
            await session.delete(result)
            await session.commit()
            return result
