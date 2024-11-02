#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :errors.py
@Time      :2024/7/30 下午10:59
@Author    :XJC
@Description:
"""
from src.core.errors import NotFoundError


class DnsNotFoundError(NotFoundError):
    entity_name: str = "数据源"
