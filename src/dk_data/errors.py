#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :errors.py
@Time      :2024/11/29 14:18
@Author    :XJC
@Description:
"""
from src.core.error import NotFoundError


class DnsNotFoundError(NotFoundError):
    entity_name: str = "数据源"