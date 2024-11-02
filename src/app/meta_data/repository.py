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
from sqlalchemy.orm import Session, backref, joinedload, relationship

from .errors import DnsNotFoundError
from .models import DkCatalog, DkDataSourcesInfo, DkTableInfo


class DnsTypeRepository:
    """数据源类型"""
    ...


class DnsRepository:
    """
    数据源crud
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self):
        with self.session_factory() as session:
            query = select(DkDataSourcesInfo).order_by(DkDataSourcesInfo.id)
            result = paginate(session, query)
            return result.model_dump()

    def get_by_id(self, dns_id: str) -> DkDataSourcesInfo:
        with self.session_factory() as session:
            query = select(DkDataSourcesInfo).where(DkDataSourcesInfo.id == dns_id)
            result = session.execute(query)
            result = result.scalar()
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, dns_id)
            return result

    def delete_by_id(self, dns_id: str) -> Type[DkDataSourcesInfo]:
        with self.session_factory() as session:
            result = session.get(DkDataSourcesInfo, dns_id)
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, dns_id)
            session.delete(result)
            session.commit()
            return result


class DkCatalogRepository:
    """
    数据目录crud
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self):
        with self.session_factory() as session:
            query = select(DkCatalog).order_by(DkCatalog.id)
            result = paginate(session, query)
            return result.model_dump()

    def get_by_id(self, catalog_id: str) -> DkCatalog:
        with self.session_factory() as session:
            query = select(DkCatalog).where(DkCatalog.id == catalog_id)
            result = session.execute(query)
            result = result.scalar()
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, catalog_id)
            return result

    def delete_by_id(self, catalog_id: str) -> Type[DkCatalog]:
        with self.session_factory() as session:
            result = session.get(DkCatalog, catalog_id)
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, catalog_id)
            session.delete(result)
            session.commit()
            return result


class DkTableInfoRepository:
    """
    表管理crud
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_table_all(self):
        with self.session_factory() as session:
            query = select(DkTableInfo).options(joinedload(DkTableInfo.fields,innerjoin=True))
            result = paginate(session, query)
            return result.model_dump()
