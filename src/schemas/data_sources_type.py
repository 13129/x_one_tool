#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :data_sources_type.py
@Time      :2024/3/1 17:34
@Author    :XJC
@Description:
"""
from __future__ import annotations

from typing import Optional

from pydantic import Field, BaseModel
from pydantic.alias_generators import to_camel


class DkDataSourcesTypeSchema(BaseModel):
    id: Optional[str]=Field(title="主键")
    type_name: str
    is_async: Optional[int]
    connect_string_default: Optional[str]
    delete_status: int

    class Config:
        from_attributes = True
        # alias_generator = to_camel
        populate_by_name = True

