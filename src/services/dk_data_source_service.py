#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :services.py
@Time      :2024/7/30 下午6:36
@Author    :XJC
@Description:
"""
from typing import Type

from src.models import DkDataSourcesInfo
from src.repositories import DnsRepository


class DnsService:

    def __init__(self, repository: DnsRepository) -> None:
        self._repository: DnsRepository = repository

    async def get_all(self) -> list[Type[DkDataSourcesInfo]]:
        return await self._repository.get_all()

    async def get_one(self, _id: str) -> DkDataSourcesInfo:
        return await self._repository.get_one(_id)

    async def delete_one(self, _id: str) -> Type[DkDataSourcesInfo]:
        return await self._repository.delete_one(_id)
