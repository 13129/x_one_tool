# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :data_tables.py
@Time      :2024/2/4 9:42
@Author    :XJC
@Description:
"""
import enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

from src.core import BaseModelSchema


class DataTableTypeEnum(str, enum.Enum):
    Delete = "删除表"
    Temp = "临时表"
    View = "视图"
    DefaultTable = "普通表"


class DkFieldInfoSchema(BaseModelSchema):
    """
    字段创建
    """
    table_code: int
    physical_table_name: str
    name_en: str
    name_cn: str
    is_pk: bool
    is_show_list: bool
    is_show_detail: bool
    order_no: int
    type: str
    domain_value: str
    is_image: bool
    create_time: datetime
    last_modify_time: datetime

    class Config:
        from_attributes = True
        # alias_generator = to_camel
        populate_by_name = True


class DkTableSchema(BaseModelSchema):
    """
    表字段创建
    """
    datasource_id: str
    name: str
    physical_table_name: str
    logic_table_name: str
    table_name_alias: str
    table_code: int
    table_type: DataTableTypeEnum = DataTableTypeEnum.DefaultTable
    is_open: bool
    is_edit: bool
    order_no: int
    creator: str
    last_modifier: str
    create_time: datetime
    last_modify_time: datetime

    # fields_info: List[DkFieldInfoSchemaCreate] = []
    class Config:
        from_attributes = True
        # alias_generator = to_camel
        populate_by_name = True
#
#
# class DkTableFieldDetailSchema(DkTableFieldDetailSchemaCreate):
#     """
#     表字段详情
#     """
#     create_time: datetime
#     last_modify_time: datetime
#     fields_info: List["DkFieldInfoSchema"] = []
#
#     class Config:
#         from_attributes = True
#         alias_generator = to_camel
#         populate_by_name = True
#
#
# class DkFieldInfoSchema(DkFieldInfoSchemaCreate):
#     create_time: datetime
#     last_modify_time: datetime
#
#     class Config:
#         from_attributes = True
#         alias_generator = to_camel
#         populate_by_name = True
