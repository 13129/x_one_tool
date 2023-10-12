"""
coding:utf-8
@Time:2022/8/4 23:26
@Author:XJC
@Description:
"""
import uuid

from pydantic import Field, BaseModel, field_validator
from ipaddress import IPv4Address
from datetime import datetime
from typing import List
from pydantic.functional_serializers import PlainSerializer

from typing_extensions import Annotated

FancyInt = Annotated[
    IPv4Address, PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]


class DkDnsTypeSchemaCreate(BaseModel):
    type_name: str
    connect_string_default: str
    delete_status: bool = Field(default=True)

    class Config:
        from_attributes = True


class DkDnsSchemaCreate(BaseModel):
    datasource_type_id: str
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
    last_modifier: str

    class Config:
        from_attributes = True

    @field_validator('host')
    def name_must_contain_space(cls, v):
        return str(v)


class DkTableSchemaCreate(BaseModel):
    datasource_id: str
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
    last_modifier: str

    class Config:
        from_attributes = True


from apps.base import BaseModelSchema


class DkCatalogTableNextSchema(BaseModelSchema):
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
    # ctl_tb_relation_info: List[DkCatalogTableRelationalSchema]
    child_info: List["DkCatalogTableNextSchema"] = []  # noqa: F401

    class Config:
        from_attributes = True
