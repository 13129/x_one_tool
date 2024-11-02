#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :containers.py
@Time      :2024/7/30 下午6:37
@Author    :XJC
@Description:
"""
from dependency_injector import containers, providers

from src.core.containers import BaseContainer
from .repositories import DkTableInfoRepository, DnsRepository
from .services import DkTableInfoService, DnsService


class MetaDataManagerContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=[".routers"])
    dns_repository = providers.Factory(
        DnsRepository,
        session_factory=BaseContainer.db.provided.session,
    )
    dns_service = providers.Factory(
        DnsService,
        repository=dns_repository,
    )

    table_repository = providers.Factory(
        DkTableInfoRepository,
        session_factory=BaseContainer.db.provided.session,
    )
    table_service = providers.Factory(
        DkTableInfoService,
        repository=table_repository,
    )
