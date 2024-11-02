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
from typing import List, Optional

from pydantic.alias_generators import to_camel
from pydantic.fields import Field

from src.core import BaseModelSchema


class DkCatalogRelSchemaDetail(BaseModelSchema):
    name_cn: Optional[str]
    name_en: Optional[str]
    catalog_code: Optional[str]
    order_no: int
    is_show: bool
    creator: str
    create_time: datetime
    last_modifier: str
    last_modify_time: datetime
    child_info: Optional[List[DkCatalogRelSchemaDetail]]

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
