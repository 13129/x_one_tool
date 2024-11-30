#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :routers.py
@Time      :2024/7/30 下午7:12
@Author    :XJC
@Description:
"""
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query
from fastapi_pagination import Page, pagination_ctx
from src.core.dependency import CustomPage
from src.common import RestGet, VControllerBase
from src.core import ResultJson
from src.core.error import NotFoundError
from src.schemas import DkDataSourcesSchema
from src.containers import DkDnsContainer


class DkDnsRouter(VControllerBase):
    """
    管理数据源
    """
    prefix = "dataSourcesInfo"
    tags = ["数据源"]
    page = CustomPage
    response_schema = DkDataSourcesSchema
    dnsService = Provide[DkDnsContainer.service]
    logger = Provide[DkDnsContainer.logger]

    @RestGet(path='/getDataSources',
             summary='获取数据源',
             dependencies=[Depends(dependency=pagination_ctx(page=page))],
             response_model=ResultJson[page[response_schema]])
    async def ov_get_all(self):
        result = await self.dnsService.get_all()
        return ResultJson(data=result)

    @RestGet(path='/getDataSourceInfo/{dns_id}',
             summary="数据源详情",
             response_model=ResultJson[response_schema])
    async def ov_get_one(self, dns_id: str):
        try:
            result = await self.dnsService.get_one(dns_id)
        except NotFoundError as e:
            return ResultJson(code=e.status_code, data=None, message=e.detail)
        else:
            return ResultJson(data=result)
