"""
coding:utf-8
@Time:2022/8/4 23:30
@Author:XJC
@Description:
"""
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from apps.common import SQLAlchemyCRUDRouter as CRUDRouter
from apps.db import get_db
from apps.db_catlog.models import (DkDNSType, DkDataSourceInfo, DkCatalogTableRelational, DkCatalogTable, DkCatalog)
from apps.db_catlog.repositories import (DkDnsTypeSchema, DkDnsSchema, DkCatalogTableRelationalSchema,
                                         DkTableSchema, DkCatalogSchema)
from apps.db_catlog.schemas import DkDnsTypeSchemaCreate, DkTableSchemaCreate, DkDnsSchemaCreate


class DkDnsTypeRouter:
    router = CRUDRouter(schema=DkDnsTypeSchema, create_schema=DkDnsTypeSchemaCreate, db_model=DkDNSType,
                        db=get_db,
                        update_route=False, delete_all_route=False, delete_one_route=False,
                        tags=["元数据"], prefix='dataDnsTypes')


# @cbv(dk_dns_router)
class DkDnsRouter:
    router = CRUDRouter(schema=DkDnsSchema, create_schema=DkDnsSchemaCreate, db_model=DkDataSourceInfo,
                        db=get_db,
                        tags=["数据源"], prefix='dataDns',
                        get_all_route=False, get_one_route=False)

    @staticmethod
    @router.get('', summary='获取全部数据源')
    async def overloaded_dk_dns_get_all(pagination=router.pagination, session=Depends(router.db_func)):
        skip, limit = pagination.get("skip"), pagination.get("limit")
        query = select(DkDataSourceInfo).options(
            joinedload(DkDataSourceInfo.datasource_type, innerjoin=True)).order_by(DkDataSourceInfo.id).limit(
            limit).offset(skip)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @router.get('/{item_id}', summary='获取数据源详情')
    async def overloaded_dk_dns_get_one(item_id=None, session=Depends(router.db_func)):
        query = select(DkDataSourceInfo).options(
            joinedload(DkDataSourceInfo.datasource_type_info, innerjoin=True)).where(
            DkDataSourceInfo.id == item_id)
        result = await session.execute(query)
        return result.scalars().all()


class DkTableRouter:
    router = CRUDRouter(schema=DkTableSchema, create_schema=DkTableSchemaCreate, db_model=DkCatalogTable,
                        db=get_db,
                        get_all_route=False, tags=["表管理"], prefix='dataTables')

    @staticmethod
    @router.get('', summary='获取所有表列表')
    async def overloaded_dk_table_get_all(pagination=router.pagination, session=Depends(router.db_func)):
        skip, limit = pagination.get("skip"), pagination.get("limit")
        query = select(DkCatalogTable).options(
            joinedload(DkCatalogTable.datasource_info, innerjoin=True)).order_by(
            DkCatalogTable.id).limit(
            limit).offset(skip)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @router.get('/{item_id}', summary='获取表详情')
    async def overloaded_dk_table_get_one(item_id=None, session=Depends(router.db_func)):
        query = select(DkCatalogTable).options(
            joinedload(DkCatalogTable.field_info, innerjoin=True)).options(
            joinedload(DkCatalogTable.datasource_info, innerjoin=True)).where(DkCatalogTable.id == item_id)

        result = await session.execute(query)
        return result.scalars().unique().all()


class DkCatalogRouter:
    router = CRUDRouter(schema=DkCatalogSchema, db_model=DkCatalog, db=get_db, tags=["目录管理"], prefix='dataCatalogs')

    @staticmethod
    @router.get('', summary='获取全部目录')
    async def overloaded_dk_catalog_get_all(session=Depends(router.db_func)):
        query = select(DkCatalog).options(
            joinedload(DkCatalog.child_info, innerjoin=True)).order_by(DkCatalog.order_no)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    @router.get('/{item_id}', summary='获取目录详情')
    async def overloaded_dk_catalog_get_all(item_id: str = None, session=Depends(router.db_func)):
        query = select(DkCatalog).options(
            joinedload(DkCatalog.child_info, innerjoin=True)).where(
            DkCatalog.id == item_id).order_by(
            DkCatalog.order_no)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    @router.api_route('/catalogTableRelationList/', methods=['GET'], summary='获取目录与表关联清单列表',
                      # response_model=DkCatalogSchema
                      )
    async def dk_catalog_table_relation_get_all(session=Depends(router.db_func)):
        # print(help(DkCatalogTableRelational.catalog_info))
        query = select(DkCatalog).options(
            joinedload(DkCatalog.child_info, innerjoin=True)
            # .options(
            #     joinedload(DkCatalogTableRelationalRouter.router.db_model.catalog_info, innerjoin=True).options(joinedload(
            #         DkCatalogTableRelationalRouter.router.db_model.table_info)))
        ).options(
            joinedload(DkCatalogTableRelational.catalog_info, innerjoin=True)
            # .options(joinedload(
            #     DkCatalogTableRelational.catalog_info))
        )

        result = await session.execute(query)
        result = jsonable_encoder(result.scalars().unique().all())

        return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})


class DkCatalogTableRelationalRouter:
    router = CRUDRouter(schema=DkCatalogTableRelationalSchema, db_model=DkCatalogTableRelational,
                        db=get_db, get_all_route=False, get_one_route=False,
                        tags=["目录关联管理"], prefix='catalogTableRelations')

# class DkDataQueryRouter:
#     router = CRUDRouter(schema=DkCatalogSchema, db_model=DkCatalog, db=get_db, tags=["数据检索服务"],
#                         prefix='/dataPools')
#
#     @staticmethod
#     @router.api_route('/queryData/', methods=['POST'], summary='数据池数据查询')
#     async def dk_query_data(session=Depends(router.db_func)):
#         query = select(DkCatalogTable).options(
#             joinedload(DkCatalogRouter.router.db_model.child_info, innerjoin=True).options(
#                 joinedload(DkCatalogRouter.router.db_model.ctl_tb_relation_info, innerjoin=True).options(joinedload(
#                     DkCatalogTableRelationalRouter.router.db_model.table_info)))).options(
#             joinedload(DkCatalogRouter.router.db_model.ctl_tb_relation_info, innerjoin=True).options(joinedload(
#                 DkCatalogTableRelationalRouter.router.db_model.table_info).options(
#                 joinedload(DkTableRouter.router.db_model.datasource_info))))
#
#         result = await session.execute(query)
#         result = jsonable_encoder(result.scalars().unique().all())
#
#         return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})
