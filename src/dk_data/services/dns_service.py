#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :dns_service.py
@Time      :2024/11/29 14:12
@Author    :XJC
@Description:
"""

from typing import Sequence, Type

from src.dk_data.db_model.dns_model import DkCatalog, DkDataSourcesInfo, DkTableInfo
from src.dk_data.repositories.dns_repository import DkCatalogRepository, DkTableInfoRepository, DnsRepository
from src.dk_data.interfaces.dns_interface import DnsServiceInterface


class DnsService(DnsServiceInterface):

    def __init__(self, repository: DnsRepository) -> None:
        self._repository: DnsRepository = repository

    async def get_all(self) -> list[Type[DkDataSourcesInfo]]:
        return await self._repository.get_all()

    async def get_one(self, _id: str) -> DkDataSourcesInfo:
        return await self._repository.get_one(_id)

    async def delete_one(self, _id: str) -> DkDataSourcesInfo:
        return await self._repository.delete_one(_id)


class DkTableInfoService:

    def __init__(self, repository: DkTableInfoRepository) -> None:
        self._repository: DkTableInfoRepository = repository

    async def get_all(self) -> list[Type[DkTableInfo]]:
        return await self._repository.get_all()


class DkCatalogService:

    def __init__(self, repository: DkCatalogRepository) -> None:
        self._repository: DkCatalogRepository = repository

    async def get_all(self) -> Sequence[DkCatalog]:
        return await self._repository.get_all()

    async def get_one(self, _id: str) -> DkCatalog:
        return await self._repository.get_one(_id)

    async def delete_one(self, _id: str) -> Type[DkCatalog]:
        return await self._repository.delete_one(_id)
