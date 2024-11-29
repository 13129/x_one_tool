#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :services.py
@Time      :2024/11/29 14:12
@Author    :XJC
@Description:
"""

from typing import Type

from .models import DkCatalog,DkDataSourcesInfo,DkTableInfo
from .repositories import DkCatalogRepository,DkTableInfoRepository,DnsRepository


class DnsService:

    def __init__(self, repository: DnsRepository) -> None:
        self._repository: DnsRepository = repository

    async def get_all(self) -> list[Type[DkDataSourcesInfo]]:
        return await self._repository.get_all()

    async def get_one(self, _id: str) -> DkDataSourcesInfo:
        return await self._repository.get_one(_id)

    async def delete_one(self, _id: str) -> Type[DkDataSourcesInfo]:
        return await self._repository.delete_one(_id)



class DkTableInfoService:

    def __init__(self, repository: DkTableInfoRepository) -> None:
        self._repository: DkTableInfoRepository = repository

    async def get_all(self) -> list[Type[DkTableInfo]]:
        return await self._repository.get_all()




class DkCatalogService:

    def __init__(self, repository: DkCatalogRepository) -> None:
        self._repository: DkCatalogRepository = repository

    async def get_all(self, name) -> list[DkCatalog]:
        return await self._repository.get_all(name)

    async def get_one(self, _id: str) -> DkCatalog:
        return await self._repository.get_one(_id)

    async def delete_one(self, _id: str) -> Type[DkCatalog]:
        return await self._repository.delete_one(_id)