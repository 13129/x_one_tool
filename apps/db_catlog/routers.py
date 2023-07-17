"""
coding:utf-8
@Time:2022/8/4 23:30
@Author:XJC
@Description:
"""
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from apps.base import cbv
from apps.db_catlog.customs import (dk_dns_router, dk_table_router, dk_catalog_router, dk_dns_type_router,
                                    dk_catalog_table_relation)


@cbv(dk_dns_type_router)
class DkDnsTypeRouter:
    pass


@cbv(dk_dns_router)
class DkDnsRouter:
    @dk_dns_router.get('', summary='获取全部数据源')
    async def overloaded_dk_dns_get_all(self, pagination=dk_dns_router.pagination,
                                        session=Depends(dk_dns_router.db_func)):
        skip, limit = pagination.get("skip"), pagination.get("limit")
        query = select(self.router.db_model).options(
            joinedload(self.router.db_model.datasource_type, innerjoin=True)).order_by(
            self.router.db_model.id).limit(
            limit).offset(skip)
        result = await session.execute(query)
        return result.scalars().all()

    @dk_dns_router.get('/{item_id}', summary='获取数据源详情')
    async def overloaded_dk_dns_get_one(self, session=Depends(dk_dns_router.db_func), item_id=None):
        query = select(self.router.db_model).options(
            joinedload(self.router.db_model.datasource_type, innerjoin=True)).where(
            self.router.db_model.id == item_id)
        result = await session.execute(query)
        return result.scalars().first()


@cbv(dk_table_router)
class DkTableRouter:
    @dk_table_router.get('', summary='获取所有表列表')
    async def overloaded_dk_table_get_all(self, pagination=dk_table_router.pagination,
                                          session=Depends(dk_table_router.db_func)):
        skip, limit = pagination.get("skip"), pagination.get("limit")
        query = select(self.router.db_model).options(
            joinedload(self.router.db_model.datasource, innerjoin=True)).order_by(
            self.router.db_model.id).limit(
            limit).offset(skip)
        result = await session.execute(query)
        return result.scalars().all()

    @dk_table_router.get('/{item_id}', summary='获取表详情')
    async def overloaded_dk_table_get_one(self, session=Depends(dk_table_router.db_func), item_id=None):
        query = select(self.router.db_model).options(
            joinedload(self.router.db_model.fields, innerjoin=True)).options(
            joinedload(self.router.db_model.datasource, innerjoin=True)).where(
            self.router.db_model.id == item_id)

        result = await session.execute(query)
        return result.scalars().unique().all()


@cbv(dk_catalog_router)
class DkCatalogRouter:

    @dk_catalog_router.get('', summary='获取全部目录')
    async def overloaded_dk_catalog_get_all(self, session=Depends(dk_catalog_router.db_func)):
        query = select(self.router.db_model).options(
            joinedload(self.router.db_model.parents, innerjoin=True)).order_by(
            self.router.db_model.order_no)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @dk_catalog_router.get('/{item_id}', summary='获取目录详情')
    async def overloaded_dk_catalog_get_all(self, session=Depends(dk_catalog_router.db_func), item_id: str = None):
        query = select(self.router.db_model).options(
            joinedload(self.router.db_model.parents, innerjoin=True)).where(
            self.router.db_model.id == item_id).order_by(
            self.router.db_model.order_no)
        result = await session.execute(query)
        return result.scalars().unique().all()


@cbv(dk_catalog_table_relation)
class DkCatalogTableRelationalRouter:
    pass
