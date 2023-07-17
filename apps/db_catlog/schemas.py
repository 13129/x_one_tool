"""
coding:utf-8
@Time:2022/8/4 23:26
@Author:XJC
@Description:
"""
from pydantic import Field, BaseModel
from ipaddress import IPv4Address
from datetime import datetime


class DkDnsTypeSchemaCreate(BaseModel):
    type_name: str
    connect_string_default: str
    delete_status: bool = Field(default=True)

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


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
        orm_mode = True
