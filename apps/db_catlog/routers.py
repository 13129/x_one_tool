"""
coding:utf-8
@Time:2022/8/4 23:30
@Author:XJC
@Description:
"""
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from apps.common import SQLAlchemyCRUDRouter as CRUDRouter
from apps.db import get_db
from apps.db_catlog.models import (DkDNSType, DkDataSourceinfo, DkCatalogTableRelational, DkCatalogTable, DkCatalog)
from apps.db_catlog.repositories import (DkDnsTypeSchema, DkDnsSchema, DkCatalogTableRelationalSchema,
                                         DkTableSchema, DkCatalogSchema)
from apps.db_catlog.schemas import DkDnsTypeSchemaCreate, DkTableSchemaCreate, DkDnsSchemaCreate


class DkDnsTypeRouter:
    router = CRUDRouter(schema=DkDnsTypeSchema, create_schema=DkDnsTypeSchemaCreate, db_model=DkDNSType,
                        db=get_db,
                        update_route=False, delete_all_route=False, delete_one_route=False,
                        tags=["元数据"])
    # @classmethod
    # @router.get('/test', summary='获取全部元数据')
    # async def test(cls):
    #     print("测试")
    #     return {"1":200}


# @cbv(dk_dns_router)
class DkDnsRouter:
    router = CRUDRouter(schema=DkDnsSchema, create_schema=DkDnsSchemaCreate, db_model=DkDataSourceinfo,
                        db=get_db,
                        tags=["数据源"],
                        get_all_route=False, get_one_route=False)

    @staticmethod
    @router.get('', summary='获取全部数据源')
    async def overloaded_dk_dns_get_all(pagination=router.pagination, session=Depends(router.db_func)):
        skip, limit = pagination.get("skip"), pagination.get("limit")
        query = select(DkDnsRouter.router.db_model).options(
            joinedload(DkDnsRouter.router.db_model.datasource_type, innerjoin=True)).order_by(
            DkDnsRouter.router.db_model.id).limit(
            limit).offset(skip)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @router.get('/{item_id}', summary='获取数据源详情')
    async def overloaded_dk_dns_get_one(item_id=None, session=Depends(router.db_func)):
        query = select(DkDnsRouter.router.db_model).options(
            joinedload(DkDnsRouter.router.db_model.datasource_type, innerjoin=True)).where(
            DkDnsRouter.router.db_model.id == item_id)
        result = await session.execute(query)
        return result.scalars().all()


class DkTableRouter:
    router = CRUDRouter(schema=DkTableSchema, create_schema=DkTableSchemaCreate, db_model=DkCatalogTable,
                        db=get_db,
                        get_all_route=False, tags=["表管理"])

    @staticmethod
    @router.get('', summary='获取所有表列表')
    async def overloaded_dk_table_get_all(pagination=router.pagination, session=Depends(router.db_func)):
        skip, limit = pagination.get("skip"), pagination.get("limit")
        query = select(DkTableRouter.router.db_model).options(
            joinedload(DkTableRouter.router.db_model.datasource, innerjoin=True)).order_by(
            DkTableRouter.router.db_model.id).limit(
            limit).offset(skip)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @router.get('/{item_id}', summary='获取表详情')
    async def overloaded_dk_table_get_one(item_id=None, session=Depends(router.db_func)):
        query = select(DkTableRouter.router.db_model).options(
            joinedload(DkTableRouter.router.db_model.fields, innerjoin=True)).options(
            joinedload(DkTableRouter.router.db_model.datasource, innerjoin=True)).where(
            DkTableRouter.router.db_model.id == item_id)

        result = await session.execute(query)
        return result.scalars().unique().all()


class DkCatalogRouter:
    router = CRUDRouter(schema=DkCatalogSchema, db_model=DkCatalog, db=get_db, tags=["目录管理"])

    @staticmethod
    @router.get('', summary='获取全部目录')
    async def overloaded_dk_catalog_get_all(session=Depends(router.db_func)):
        query = select(DkCatalogRouter.router.db_model).options(
            joinedload(DkCatalogRouter.router.db_model.parents, innerjoin=True)).order_by(
            DkCatalogRouter.router.db_model.order_no)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    @router.get('/{item_id}', summary='获取目录详情')
    async def overloaded_dk_catalog_get_all(item_id: str = None, session=Depends(router.db_func)):
        query = select(DkCatalogRouter.router.db_model).options(
            joinedload(DkCatalogRouter.router.db_model.parents, innerjoin=True)).where(
            DkCatalogRouter.router.db_model.id == item_id).order_by(
            DkCatalogRouter.router.db_model.order_no)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    @router.api_route('/catalog_table_relation/', methods=['GET'], summary='获取目录与表关联列表')
    async def dk_catalog_table_relation_get_all(session=Depends(router.db_func)):
        print('测试')
        query = select(DkCatalogRouter.router.db_model).options(
            joinedload(DkCatalogRouter.router.db_model.parents, innerjoin=True)).options(
            joinedload(DkCatalogRouter.router.db_model.ctl_tables, innerjoin=True))
        print('测试', query)
        result = await session.execute(query)
        return result.scalars().unique().all()


class DkCatalogTableRelationalRouter:
    router = CRUDRouter(schema=DkCatalogTableRelationalSchema, db_model=DkCatalogTableRelational,
                        db=get_db, get_all_route=False, get_one_route=False,
                        tags=["目录关联管理"])
#
#     @staticmethod
#     @router.get('', summary='获取全部目录表关联')
#     async def overload_dk_catalog_get_all(session=Depends(router.db_func)):
#         query = select(DkCatalogTableRelationalRouter.router.db_model).options(
#             joinedload(DkCatalogTableRelationalRouter.router.db_model.parents, innerjoin=True)).options(
#             joinedload(DkCatalogTableRelationalRouter.router.db_model.catalog_table, innerjoin=True)).order_by(
#             DkCatalogTableRelationalRouter.router.db_model.order_no)
#         result = await session.execute(query)
#         return result.scalars().unique().all()
