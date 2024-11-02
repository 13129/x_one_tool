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
    Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))
    response_schema = DkDataSourcesSchema
    dns_service = Provide[DkDnsContainer.service]
    logger = Provide[DkDnsContainer.logger]

    @RestGet(
        path='/getDataSources',
        summary='获取数据源',
        dependencies=[Depends(pagination_ctx(Page))],
        response_model=ResultJson[Page[response_schema]])
    def ov_get_all(self):
        result = self.dns_service.get_all()
        return ResultJson(data=result)

    @RestGet(
        path='/getDataSourceInfo/{dns_id}',
        summary="数据源详情",
        response_model=ResultJson[response_schema])
    def ov_get_one(self, dns_id: str):
        try:
            result = self.dns_service.get_one(dns_id)
        except NotFoundError as e:
            return ResultJson(code=e.status_code, data=None, message=e.detail)
        else:
            return ResultJson(data=result)