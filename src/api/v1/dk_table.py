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
from src.schemas import DkTableSchema
from src.containers import DkTableContainer


class DkTableRouter(VControllerBase):
    prefix = "dkTableInfo"
    tags = ["数据表"]
    Page = Page.with_custom_options(size=Query(10, ge=1, le=100, description="Page size limit"))
    response_schema = DkTableSchema
    table_service = Provide[DkTableContainer.service]
    logger = Provide[DkTableContainer.logger]

    @RestGet(
        path='/getTableList',
        summary='获取数据表',
        dependencies=[Depends(pagination_ctx(Page))],
        response_model=ResultJson[Page[response_schema]])
    def ov_get_data_table_info_all(self):
        result = self.table_service.get_table_all()
        self.logger.info(result)
        return ResultJson(data=result)
