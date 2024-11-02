#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :__init__.py.py
@Time      :2024/7/30 下午6:33
@Author    :XJC
@Description:
"""
from fastapi import APIRouter

from src.app.dns.routers import DkDnsRouter, DkTableRouter

dns_api = APIRouter()
dns_api.include_router(DkDnsRouter.instance(), prefix="/dataSources")
dns_api.include_router(DkTableRouter.instance(), prefix="/dataSources")