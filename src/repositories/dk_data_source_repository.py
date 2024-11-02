
from contextlib import AbstractContextManager
from typing import Callable, Type

from fastapi import status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.errors import DnsNotFoundError
from src.models import  DkDataSourcesInfo


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
            query = select(DkDataSourcesInfo).order_by(DkDataSourcesInfo.last_modify_time)
            result = paginate(session, query)
            return result.model_dump()

    def get_one(self, _id: str) -> DkDataSourcesInfo:
        with self.session_factory() as session:
            query = select(DkDataSourcesInfo).where(DkDataSourcesInfo.id == _id)
            result = session.execute(query)
            result = result.scalar()
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, _id)
            return result

    def delete_one(self, _id: str) -> Type[DkDataSourcesInfo]:
        with self.session_factory() as session:
            result = session.get(DkDataSourcesInfo, _id)
            if not result:
                raise DnsNotFoundError(status.HTTP_404_NOT_FOUND, None, None, _id)
            session.delete(result)
            session.commit()
            return result