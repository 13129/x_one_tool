#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :__init__.py.py
@Time      :2024/7/26 下午8:11
@Author    :XJC
@Description:
"""

from setting import settings
from src.api import dk_api

from src.containers import DkDnsContainer, DkTableContainer
from src.core.container import BaseContainer
from .module import Application


def init_di(app):
    container = Application()
    container.wire(modules=[__name__])
    app.container = container
    app.include_router(dk_api, prefix=settings.API_V1_STR)

    return app
