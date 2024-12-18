#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :dk_data.py
@Time      :2024/11/29 14:31
@Author    :XJC
@Description:
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.alias_generators import to_camel
from pydantic.fields import Field

from src.core import BaseModelSchema


class DkDataSourcesTypeSchema(BaseModel):
    id: Optional[str] = Field(title="主键")
    type_name: str
    is_async: Optional[int]
    connect_string_default: Optional[str]
    delete_status: int

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class DataSourceTypeEnum(str, enum.Enum):
    PostgreSQL = "PostgreSQL"
    MySQL = "MySQL"
    Oracle = "Oracle"
    Kafka = "Kafka"
    Ftp = "FTP"
    SFtp = "SFTP"



class DkDataSourcesSchemaCreate(BaseModelSchema):
    datasource_type_id: DataSourceTypeEnum = DataSourceTypeEnum.PostgreSQL
    datasource_name: str
    host: str
    user_name: str
    password: str
    connect_string: str
    driver_name: str
    default_db: str
    driver_file_path: str
    port: int
    creator: str
    last_modifier: str

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class DkDataSourcesSchema(DkDataSourcesSchemaCreate):
    id: str
    create_time: datetime
    last_modify_time: datetime

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


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


class DkCatalogRelSchemaDetail(BaseModelSchema):
    name_cn: Optional[str]
    name_en: Optional[str]
    catalog_code: Optional[str]
    parent_id:Optional[str]
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

