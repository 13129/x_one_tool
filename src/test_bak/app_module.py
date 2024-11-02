#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :app_module.py
@Time      :2024/7/30 下午7:00
@Author    :XJC
@Description:
"""
from dependency_injector import providers

from .meta_data.container import MetaDataManagerContainer
from src.core.container import BaseContainer


class Application(BaseContainer):
    MetaDataManagerModule = providers.Container(
        MetaDataManagerContainer,
    )
