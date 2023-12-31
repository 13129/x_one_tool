"""
coding:utf-8
@Time:2022/8/4 23:30
@Author:XJC
@Description:
"""

from fastapi import Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from apps.common import SQLAlchemyCRUDRouter as CRUDRouter
from apps.db import get_db
from apps.db_catlog.models import (DkDNSType, DkDnsInfo, DkCatalogTableRelational, DkCatalogTable, DkCatalog)
from apps.db_catlog.repositories import (DkDnsTypeSchema, DkDnsSchema, DkCatalogTableRelationalSchema,
                                         DkTableSchema, DkCatalogSchema, OutDkCatalogSchema)
from apps.db_catlog.schemas import DkDnsTypeSchemaCreate, DkTableSchemaCreate, DkDnsSchemaCreate


class DkDnsTypeRouter:
    """
    用于管理数据源驱动的增删改查
    """
    router = CRUDRouter(schema=DkDnsTypeSchema, create_schema=DkDnsTypeSchemaCreate, db_model=DkDNSType,
                        db=get_db,
                        update_route=False, delete_all_route=False, delete_one_route=False, get_all_route=True,
                        tags=["元数据"], prefix='dataDnsTypes')

    Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))

    @staticmethod
    @router.get('', summary='获取全部元数据', response_model=Page[router.schema])
    async def overloaded_dk_dns_type_get_all(session=Depends(router.db_func)):
        query = select(DkDNSType).order_by(DkDNSType.id)
        return await paginate(session, query)


class DkDnsRouter:
    """
    用于管理数据源的增删改查
    """
    router = CRUDRouter(schema=DkDnsSchema, create_schema=DkDnsSchemaCreate, db_model=DkDnsInfo,
                        db=get_db,
                        tags=["数据源"], prefix='dataDns',
                        get_all_route=False, get_one_route=False)
    Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))

    @staticmethod
    @router.get('', summary='获取全部数据源', response_model=Page[router.schema])
    async def overloaded_dk_dns_get_all(session=Depends(router.db_func)):
        query = select(DkDnsInfo).options(
            joinedload(DkDnsInfo.datasource_type_info, innerjoin=True)).order_by(DkDnsInfo.id)
        return await paginate(session, query)

    @staticmethod
    @router.get('/{item_id}', summary='获取数据源详情')
    async def overloaded_dk_dns_get_one(item_id=None, session=Depends(router.db_func)):
        query = select(DkDnsInfo).options(joinedload(DkDnsInfo.datasource_type_info, innerjoin=True)).where(
            DkDnsInfo.id == item_id)
        result = await session.execute(query)
        return result.scalars().all()


class DkTableRouter:
    """
    用于管理表元数据的增删改查
    """
    router = CRUDRouter(schema=DkTableSchema, create_schema=DkTableSchemaCreate, db_model=DkCatalogTable,
                        db=get_db,
                        get_all_route=False, tags=["表管理"], prefix='dataTables')
    Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))

    @staticmethod
    @router.get('', summary='获取所有表列表', response_model=Page[router.schema])
    async def overloaded_dk_table_get_all(session=Depends(router.db_func)):
        # limit, skip = pagination.get('limit'), pagination.get('skip')
        query = select(DkCatalogTable).options(joinedload(DkCatalogTable.datasource_info, innerjoin=True)).order_by(
            DkCatalogTable.id)
        return await paginate(session, query)
        # return result.scalars().unique().all()

    @staticmethod
    @router.get('/{item_id}', summary='获取表详情')
    async def overloaded_dk_table_get_one(item_id=None, session=Depends(router.db_func)):
        query = select(DkCatalogTable).options(joinedload(DkCatalogTable.field_info, innerjoin=False)).options(
            joinedload(DkCatalogTable.datasource_info, innerjoin=True)).where(DkCatalogTable.id == item_id)

        result = await session.execute(query)
        return result.scalars().unique().all()


class DkCatalogRouter:
    """
    用于管理目录的增删改查
    """
    router = CRUDRouter(schema=DkCatalogSchema, db_model=DkCatalog, db=get_db, tags=["目录管理"], prefix='dataCatalogs',
                        get_all_route=False)
    Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))

    @staticmethod
    @router.get('', summary='获取全部目录', response_model=Page[OutDkCatalogSchema])
    async def overloaded_dk_catalog_get_all(session=Depends(router.db_func)):
        query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True)).order_by(
            DkCatalog.order_no)
        return await paginate(session, query)

    @staticmethod
    @router.get('/{item_id}', summary='获取目录详情')
    async def overloaded_dk_catalog_get_all(item_id: str = None, session=Depends(router.db_func)):
        query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True)).where(
            DkCatalog.id == item_id).order_by(DkCatalog.order_no)
        result = await session.execute(query)
        return result.scalars().unique().all()


class DkCatalogTableRelationalRouter:
    """
    用于管理目录关联表的增删改查
    """
    router = CRUDRouter(schema=DkCatalogTableRelationalSchema, db_model=DkCatalogTableRelational,
                        db=get_db, get_all_route=False, get_one_route=False,
                        tags=["目录关联管理"], prefix='catalogTableRelations')

    @staticmethod
    @router.api_route('/catalogTableRelationList/', methods=['GET'], summary='获取目录与表关联清单列表',
                      response_model=DkCatalogSchema)
    async def dk_catalog_table_relation_get_all(session=Depends(router.db_func)):
        query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True).options(
            joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(
                joinedload(DkCatalogTableRelational.table_info)))).options(
            joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(
                joinedload(DkCatalogTableRelational.table_info)))

        result = await session.execute(query)
        result = jsonable_encoder(result.scalars().unique().all())

        return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})


class DkDataQueryRouter:
    """
    用于管理所有数据表数据的增删改查
    """
    router = CRUDRouter(schema=DkCatalogSchema, db_model=DkCatalog, db=get_db, tags=["数据检索服务"],
                        prefix='/dataPools')

    @staticmethod
    @router.api_route('/queryData/', methods=['POST'], summary='数据池数据查询')
    async def dk_query_data(session=Depends(router.db_func)):
        query = select(DkCatalog).options(
            joinedload(DkCatalog.child_info, innerjoin=True).options(
                joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(joinedload(
                    DkCatalogTableRelational.table_info)))).options(
            joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(
                joinedload(DkCatalogTableRelational.table_info).options(joinedload(DkCatalog.datasource_info))))

        result = await session.execute(query)
        result = jsonable_encoder(result.scalars().unique().all())

        return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})

    @staticmethod
    @router.api_route('/queryData/ggg/', methods=['GET'], summary='数据查询测试')
    async def dk_query_data(session=Depends(router.db_func)):
        query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True)).order_by(
            DkCatalog.order_no)
        result = await session.execute(query)
        result = jsonable_encoder(result.scalars().unique().all())

        return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})
