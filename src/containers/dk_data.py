#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :dk_data.py
@Time      :2024/11/29 14:24
@Author    :XJC
@Description:
"""

from dependency_injector import containers, providers

from src.core.container import BaseContainer
from src.dk_data.repositories import DkCatalogRepository
from src.dk_data.repositories import DkTableInfoRepository
from src.dk_data.repositories import DnsRepository
from src.dk_data.services import DkCatalogService
from src.dk_data.services import DkTableInfoService
from src.dk_data.services import DnsService



class DkDnsContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1"])
    repository = providers.Factory(
        DnsRepository,
        session_factory=BaseContainer.db.provided.dk_async_session,
    )
    service = providers.Factory(
        DnsService,
        repository=repository,
    )



class DkTableContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1"])

    repository = providers.Factory(
        DkTableInfoRepository,
        session_factory=BaseContainer.db.provided.dk_async_session,
    )
    service = providers.Factory(
        DkTableInfoService,
        repository=repository,
    )



class DkCatalogContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1"])
    repository = providers.Factory(
        DkCatalogRepository,
        session_factory=BaseContainer.db.provided.dk_async_session,
    )
    service = providers.Factory(
        DkCatalogService,
        repository=repository,
    )
