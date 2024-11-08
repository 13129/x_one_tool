#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :container.py
@Time      :2024/7/30 下午6:45
@Author    :XJC
@Description:
"""
from dependency_injector import containers, providers

from setting import settings
from src.db.db import Database
from xlogger import Logger


class BaseContainer(containers.DeclarativeContainer):
    # config = providers.Configuration(yaml_files=["config.yml"]) # 使用yml文件作为配置
    db = providers.Singleton(Database, db_url=settings.sync_database_url)
    logger = providers.Singleton(
        Logger,
        level=settings.LOG_LEVEL,
        module_name=settings.MODULE_NAME,
    )
