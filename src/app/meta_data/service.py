#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :services.py
@Time      :2024/7/30 下午6:36
@Author    :XJC
@Description:
"""
from typing import Type

from .models import DkDataSourcesInfo, DkTableInfo
from .repositories import DkTableInfoRepository
from .repositories import DnsRepository


class DnsService:

    def __init__(self, repository: DnsRepository) -> None:
        self._repository: DnsRepository = repository

    def get_dns(self) -> list[Type[DkDataSourcesInfo]]:
        return self._repository.get_all()

    def get_dns_by_id(self, dns_id: str) -> DkDataSourcesInfo:
        return self._repository.get_by_id(dns_id)

    def delete_dns_by_id(self, dns_id: str) -> Type[DkDataSourcesInfo]:
        return self._repository.delete_by_id(dns_id)


class DkTableInfoService:
    def __init__(self, repository: DkTableInfoRepository) -> None:
        self._repository: DkTableInfoRepository = repository

    def get_table_all(self) -> list[Type[DkTableInfo]]:
        return self._repository.get_table_all()
