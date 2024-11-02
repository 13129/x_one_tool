#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName    : dk_catalog_model.py
@Time    : 2024/11/2 20:44
@Author  : XJC
@Description: 
"""
from dependency_injector import containers, providers

from src.core.container import BaseContainer
from src.repositories import DkCatalogRepository
from src.services import DkCatalogService


class DkCatalogContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1"])
    repository = providers.Factory(
        DkCatalogRepository,
        session_factory=BaseContainer.db.provided.session,
    )
    service = providers.Factory(
        DkCatalogService,
        repository=repository,
    )