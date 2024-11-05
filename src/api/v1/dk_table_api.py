#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :routers.py
@Time      :2024/7/30 下午7:12
@Author    :XJC
@Description:
"""

from typing import Any
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
    page = CustomPage
    response_schema = DkTableSchema

    tableService = Provide[DkTableContainer.service]
    logger = Provide[DkTableContainer.logger]

    @RestGet(
        path='/getTableList',
        summary='获取数据表',
        dependencies=[Depends(pagination_ctx(page=page))],
        response_model=ResultJson[page[response_schema]])
    async def ov_get_all(self) -> ResultJson[Any]:
        result = await self.tableService.get_all()
        return ResultJson(data=result)

