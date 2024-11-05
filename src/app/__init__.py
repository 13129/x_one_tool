#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :__init__.py.py
@Time      :2024/7/26 下午8:11
@Author    :XJC
@Description:
"""

from setting import settings
from .app_module import Application
from .meta_data import dns_api


def init_di(app):
    container = Application()
    container.wire(modules=[__name__])
    app.container = container
    app.include_router(dns_api, prefix=settings.API_V1_STR)

    return app
