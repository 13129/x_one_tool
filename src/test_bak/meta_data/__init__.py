#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :__init__.py.py
@Time      :2024/7/30 下午6:33
@Author    :XJC
@Description:
"""
from fastapi import APIRouter

from .router import DkDnsRouter, DkTableRouter

dns_api = APIRouter()
dns_api.include_router(DkDnsRouter.instance(), prefix="/metaData")
dns_api.include_router(DkTableRouter.instance(), prefix="/metaData")
