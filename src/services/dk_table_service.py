#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :services.py
@Time      :2024/7/30 下午6:36
@Author    :XJC
@Description:
"""
from typing import Type

from src.models import DkTableInfo
from src.repositories import DkTableInfoRepository


class DkTableInfoService:

    def __init__(self, repository: DkTableInfoRepository) -> None:
        self._repository: DkTableInfoRepository = repository

    async def get_all(self) -> list[Type[DkTableInfo]]:
        return await self._repository.get_all()
