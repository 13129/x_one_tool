# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :__init__.py.py
@Time      :2024/2/4 9:04
@Author    :XJC
@Description:
"""

from .crud_base import CRUDGenerator
from .model import DBBaseModel
from .type import PYDANTIC_SCHEMA
from .schema import BaseModelSchema, RouteArgsBase, ResultJson
