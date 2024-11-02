#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :containers.py
@Time      :2024/7/30 下午6:37
@Author    :XJC
@Description:
"""
from dependency_injector import containers, providers


from src.core.container import BaseContainer
from src.repositories import DkTableInfoRepository
from src.services import DkTableInfoService


class DkTableContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1.dk_table"])

    repository = providers.Factory(
        DkTableInfoRepository,
        session_factory=BaseContainer.db.provided.session,
    )
    service = providers.Factory(
        DkTableInfoService,
        repository=repository,
    )
