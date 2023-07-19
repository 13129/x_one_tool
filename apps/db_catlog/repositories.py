"""
coding:utf-8
@Time:2022/8/4 23:28
@Author:XJC
@Description:
"""
from datetime import datetime
from ipaddress import IPv4Address
from typing import List

from apps.base import BaseModelSchema


class DkDnsTypeSchema(BaseModelSchema):
    type_name: str
    connect_string_default: str
    delete_status: bool

    class Config:
        orm_mode = True


class DkDnsSchema(BaseModelSchema):
    datasource_type_id: DkDnsTypeSchema
    datasource_name: str
    host: IPv4Address
    user_name: str
    password: str
    connect_string: str
    driver_name: str
    default_db: str
    driver_file_path: str
    port: int
    creator: str
    create_time: datetime
    last_modifier: str
    last_modify_time: datetime

    class Config:
        orm_mode = True


class DkTableSchema(BaseModelSchema):
    datasource_id: DkDnsSchema
    name: str
    physical_table_name: str
    logic_table_name: str
    table_name_alias: str
    table_code: int
    table_type: str
    is_open: bool
    is_edit: bool
    order_no: int
    creator: str
    create_time: datetime
    last_modifier: str
    last_modify_time: datetime

    class Config:
        orm_mode = True


class DkFieldSchema(BaseModelSchema):
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

    class Config:
        orm_mode = True

class DkCatalogTableRelationalSchema(BaseModelSchema):
    catalog_code_id: str
    tabl_code_id: str
    order_no: str
    is_show: bool
    creator: str
    create_time: datetime
    last_modifier: str
    last_modify_time: datetime

    class Config:
        orm_mode = True


class DkCatalogSchema(BaseModelSchema):
    name_cn: str
    name_en: str
    catalog_code: str
    parent_id: str
    order_no: int
    is_show: bool
    creator: str
    create_time: datetime
    last_modifier: str
    last_modify_time: datetime
    catalog_table: List[DkCatalogTableRelationalSchema]
    class Config:
        orm_mode = True



