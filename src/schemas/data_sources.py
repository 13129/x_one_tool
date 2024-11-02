"""
coding:utf-8
@Time:2022/8/4 23:26
@Author:XJC
@Description:
"""
from __future__ import annotations

import enum
from datetime import datetime

from src.base import BaseModelSchema


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
        # alias_generator = to_camel
        populate_by_name = True


class DkDataSourcesSchema(DkDataSourcesSchemaCreate):
    id: str
    create_time: datetime
    last_modify_time: datetime

    class Config:
        from_attributes = True
        # alias_generator = to_camel
        populate_by_name = True
