#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :dk_catalog_model.py
@Time      :2024/7/30 下午6:36
@Author    :XJC
@Description:
"""

from typing import Type, List

from src.models import DkCatalog
from src.repositories import DkCatalogRepository


class DkCatalogService:

    def __init__(self, repository: DkCatalogRepository) -> None:
        self._repository: DkCatalogRepository = repository

    def get_all(self, name) -> list[DkCatalog]:
        return self._repository.get_all(name)

    def get_by_id(self, _id: str) -> DkCatalog:
        return self._repository.get_by_id(_id)

    def delete_by_id(self, _id: str) -> Type[DkCatalog]:
        return self._repository.delete_by_id(_id)
