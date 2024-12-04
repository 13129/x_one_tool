#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :dk_data_api.py
@Time      :2024/11/29 14:27
@Author    :XJC
@Description:
"""

from typing import Any, List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi_pagination import pagination_ctx

from src.common import RestGet, VControllerBase
from src.containers.dk_data import DkCatalogContainer, DkTableContainer, DkDnsContainer
from src.core import ResultJson
from src.core.dependency import CustomPage
from src.core.error import NotFoundError
from src.schemas import DkCatalogRelSchemaDetail, DkDataSourcesSchema, DkTableSchema

class DkDnsRouter(VControllerBase):
    """
    管理数据源
    """
    prefix = "dataSourcesInfo"
    tags = ["数据源"]

    dns_service = Depends(Provide[DkDnsContainer.service])
    log = Depends(Provide[DkDnsContainer.logger])

    @RestGet(path='/getDataSources',
             summary='获取数据源',
             dependencies=[Depends(pagination_ctx(CustomPage))],
             response_model=ResultJson[CustomPage[DkDataSourcesSchema]])
    async def ov_get_all(self):
        result = await self.dns_service.get_all()
        return ResultJson(data=result)

    @RestGet(path='/getDataSourceInfo/{dns_id}',
             summary="数据源详情",
             response_model=ResultJson[DkDataSourcesSchema])
    async def ov_get_one(self, dns_id: str):
        try:
            result = await self.dns_service.get_one(dns_id)
        except NotFoundError as e:
            return ResultJson(code=e.status_code, data=None, message=e.detail)
        else:
            return ResultJson(data=result)


class DkTableRouter(VControllerBase):
    prefix = "dkTableInfo"
    tags = ["数据表"]

    tableService = Depends(Provide[DkTableContainer.service])
    log = Depends(Provide[DkTableContainer.logger])

    @RestGet(
        path='/getTableList',
        summary='获取数据表',
        dependencies=[Depends(pagination_ctx(page=CustomPage))],
        response_model=ResultJson[CustomPage[DkTableSchema]])
    async def ov_get_all(self) -> ResultJson[Any]:
        result = await self.tableService.get_all()
        return ResultJson(data=result)


class DkCatalogRouter(VControllerBase):
    prefix = "dkCatalog"
    tags = ["数据目录"]

    catalogService = Depends(Provide[DkCatalogContainer.service])
    log = Depends(Provide[DkCatalogContainer.logger])

    @RestGet(
        path='/getDkCatalogAll',
        summary='获取数据目录',
        response_model=ResultJson[List[DkCatalogRelSchemaDetail]]
    )
    @inject
    async def ov_get_all(self, catalog_service=catalogService,log=log) -> ResultJson[Any]:
        result = await catalog_service.get_all()
        log.xlog.info(result)

        # 转换为 Pydantic 模型
        def build_tree(data, parent_id=''):
            nodes = [item for item in data if item.parent_id == parent_id]
            for node in nodes:
                node.child_info = build_tree(data, parent_id=node.id)
            return nodes

        root_nodes = build_tree(result, parent_id='')
        return ResultJson(data=root_nodes)
