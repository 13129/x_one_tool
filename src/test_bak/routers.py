#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :routers.py
@Time      :2024/7/30 下午7:27
@Author    :XJC
@Description:
"""
"""
coding:utf-8
@Time:2022/8/4 23:30
@Author:XJC
@Description:
"""

# from fastapi import Depends, Query
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from fastapi_pagination import Page
# from fastapi_pagination.ext.sqlalchemy import paginate
# from sqlalchemy import select
# from sqlalchemy.orm import joinedload
#
# from src.db import get_db
# from src.dk_catlog.models import (DkDNSType, DkDnsInfo, DkCatalogTableRelational, DkCatalogTable, DkCatalog)
#
# from src.common import VirtualAPIRouter, VirtualControllerBase, RestRouteGet
# from src.dk_catlog.schemas import DkDnsTypeSchema, \
#     DkDnsSchema, DkTableSchema, DkCatalogSchema, OutDkCatalogSchema
#
#
# @VirtualAPIRouter(prefix='dataDnsTypes', tags=["元数据"])
# class DkDnsTypeRouter(VirtualControllerBase):
#     """
#     用于管理数据源驱动的增删改查
#     """
#
#     Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))
#     db = Depends(get_db)
#     schema = DkDnsTypeSchema
#
#     @RestRouteGet(path='', summary='获取全部元数据', response_model=Page[schema])
#     def ov_get_dk_dns_type_all(self, session=db):
#         query = select(DkDNSType).order_by(DkDNSType.id)
#         return paginate(session, query)

#
# @VirtualAPIRouter(prefix='dataDns', tags=["数据源"])
# class DkDnsRouter(VirtualControllerBase):
#     """
#     用于管理数据源的增删改查
#     """
#     Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))
#     db = Depends(get_db)
#     schema = DkDnsSchema
#
#     @RestRouteGet('', summary='获取全部数据源', response_model=Page[schema])
#     def overloaded_dk_dns_get_all(self, session=db):
#         query = select(DkDnsInfo).options(
#             joinedload(DkDnsInfo.datasource_type_info, innerjoin=True)).order_by(DkDnsInfo.id)
#         return paginate(session, query)
#
#     #
#     @RestRouteGet('/{item_id}', summary='获取数据源详情')
#     def overloaded_dk_dns_get_one(self, item_id=None, session=db):
#         query = select(DkDnsInfo).options(joinedload(DkDnsInfo.datasource_type_info, innerjoin=True)).where(
#             DkDnsInfo.id == item_id)
#         result = session.execute(query)
#         return result.scalars().all()
#
#
# @VirtualAPIRouter(prefix='dataTables', tags=["表管理"])
# class DkTableRouter(VirtualControllerBase):
#     """
#     用于管理表元数据的增删改查
#     """
#     Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))
#     schema = DkTableSchema
#     db = Depends(get_db)
#
#     @RestRouteGet('', summary='获取所有表列表', response_model=Page[schema])
#     def overloaded_dk_table_get_all(self, session=db):
#         query = select(DkCatalogTable).options(joinedload(DkCatalogTable.datasource_info, innerjoin=True)).order_by(
#             DkCatalogTable.id)
#         return paginate(session, query)
#
#     @RestRouteGet('/{item_id}', summary='获取表详情')
#     def overloaded_dk_table_get_one(self, item_id=None, session=db):
#         query = select(DkCatalogTable).options(joinedload(DkCatalogTable.field_info, innerjoin=False)).options(
#             joinedload(DkCatalogTable.datasource_info, innerjoin=True)).where(DkCatalogTable.id == item_id)
#
#         result = session.execute(query)
#         return result.scalars().unique().all()
#
#
# @VirtualAPIRouter(prefix='dataCatalogs', tags=["目录管理"])
# class DkCatalogRouter(VirtualControllerBase):
#     """
#     用于管理目录的增删改查
#     """
#
#     Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))
#     schema = OutDkCatalogSchema
#     db = Depends(get_db)
#
#     @RestRouteGet('', summary='获取全部目录', response_model=Page[OutDkCatalogSchema])
#     def overloaded_dk_catalog_get_all(self, session=db):
#         query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True)).order_by(
#             DkCatalog.order_no)
#         return paginate(session, query)
#
#     @RestRouteGet('/{item_id}', summary='获取目录详情')
#     def overloaded_dk_catalog_get_all(self, item_id: str = None, session=db):
#         query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True)).where(
#             DkCatalog.id == item_id).order_by(DkCatalog.order_no)
#         result = session.execute(query)
#         return result.scalars().unique().all()
#
#
# #
# @VirtualAPIRouter(prefix='catalogTableRelations', tags=["目录关联管理"])
# class DkCatalogTableRelationalRouter:
#     """
#     用于管理目录关联表的增删改查
#     """
#     db = Depends(get_db)
#     schema = DkCatalogSchema
#
#     @RestRouteGet('/catalogTableRelationList/', summary='获取目录与表关联清单列表', response_model=schema)
#     def dk_catalog_table_relation_get_all(self, session=db):
#         query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True).options(
#             joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(
#                 joinedload(DkCatalogTableRelational.table_info)))).options(
#             joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(
#                 joinedload(DkCatalogTableRelational.table_info)))
#
#         result = session.execute(query)
#         result = jsonable_encoder(result.scalars().unique().all())
#         return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})
#
#
# class DkDataQueryRouter:
#     """
#     用于管理所有数据表数据的增删改查
#     """
#     router = CRUDRouter(schema=DkCatalogSchema, db_model=DkCatalog, db=get_db, tags=["数据检索服务"],
#                         prefix='/dataPools')
#
#     @staticmethod
#     @router.api_route('/queryData/', methods=['POST'], summary='数据池查询')
#     async def dk_query_data(session=Depends(router.db_func)):
#         query = select(DkCatalog).options(
#             joinedload(DkCatalog.child_info, innerjoin=True).options(
#                 joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(joinedload(
#                     DkCatalogTableRelational.table_info)))).options(
#             joinedload(DkCatalog.ctl_tb_relation_info, innerjoin=True).options(
#                 joinedload(DkCatalogTableRelational.table_info).options(joinedload(DkCatalog.datasource_info))))
#
#         result = await session.execute(query)
#         result = jsonable_encoder(result.scalars().unique().all())
#
#         return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})
#
#     @staticmethod
#     @router.api_route('/queryData/ggg/', methods=['GET'], summary='数据查询测试')
#     async def dk_query_data(session=Depends(router.db_func)):
#         query = select(DkCatalog).options(joinedload(DkCatalog.child_info, innerjoin=True)).order_by(
#             DkCatalog.order_no)
#         result = await session.execute(query)
#         result = jsonable_encoder(result.scalars().unique().all())
#
#         return JSONResponse(status_code=200, content={"success": "ok", "code": 200, "data": result})
