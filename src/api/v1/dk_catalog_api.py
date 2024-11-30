#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName    : test.py
@Time    : 2024/11/2 20:43
@Author  : XJC
@Description: 
"""
from dependency_injector.wiring import Provide
from fastapi import Depends
from fastapi_pagination import pagination_ctx
from typing import Any, Optional
from src.common import RestGet, VControllerBase
from src.containers import DkCatalogContainer
from src.core import ResultJson
from src.core.dependency import CustomPage
from src.schemas import DkCatalogRelSchemaDetail


class DkCatalogRouter(VControllerBase):
    prefix = "dkCatalog"
    tags = ["数据目录"]

    response_schema = DkCatalogRelSchemaDetail
    catalogService = Provide[DkCatalogContainer.service]
    page = CustomPage
    logger = Provide[DkCatalogContainer.logger]

    @RestGet(
        path='/getDkCatalogAll',
        summary='获取数据目录',
        dependencies=[Depends(dependency=pagination_ctx(page=page))],
        response_model=ResultJson[page[response_schema]])
    async def ov_get_all(self, name: Optional[str] = '') -> ResultJson[Any]:
        result = await self.catalogService.get_all(name=name)
        return ResultJson(data=result)
