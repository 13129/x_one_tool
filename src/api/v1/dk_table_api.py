#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :routers.py
@Time      :2024/7/30 下午7:12
@Author    :XJC
@Description:
"""

from dependency_injector.wiring import Provide
from fastapi import Depends
from fastapi_pagination import pagination_ctx

from src.common import RestGet, VControllerBase
from src.containers import DkTableContainer
from src.core import ResultJson
from src.core.dependency import CustomPage
from src.schemas import DkTableSchema


class DkTableRouter(VControllerBase):
    prefix = "dkTableInfo"
    tags = ["数据表"]

    response_schema = DkTableSchema
    table_service = Provide[DkTableContainer.service]
    page = CustomPage
    logger = Provide[DkTableContainer.logger]

    @RestGet(
        path='/getTableList',
        summary='获取数据表',
        dependencies=[Depends(pagination_ctx(page))],
        response_model=ResultJson[page[response_schema]])
    async def ov_get_all(self):
        result = await self.table_service.get_all()
        return ResultJson(data=result)

