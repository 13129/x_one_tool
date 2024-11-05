# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :catalogs.py
@Time      :2024/2/4 9:42
@Author    :XJC
@Description:
"""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic.alias_generators import to_camel
from pydantic.fields import Field

from src.core import BaseModelSchema


class DkCatalogTableRelSchemaDetail(BaseModelSchema):
    name_cn: str
    name_en: str
    catalog_code: str
    physical_table_name: str
    table_code: int
    order_no: str
    is_edit: bool
    is_show: bool
    creator: str
    create_time: datetime
    last_modifier: str
    last_modify_time: datetime
    visual: int = Field(default=None)
    child_info: List[DkCatalogTableRelSchemaDetail] = []

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
