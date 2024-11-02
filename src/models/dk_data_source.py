#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :model.py
@Time      :2024/7/30 下午6:35
@Author    :XJC
@Description:
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from src.core import DBBaseModel


class DkDataSourcesType(DBBaseModel):
    __tablename__ = 'dk_datasource_type'
    type_name: Mapped[str] = mapped_column("type_name", String(50), comment="数据源类型名称")
    is_async: Mapped[int] = mapped_column("is_async", Boolean, comment="是否异步", default=0)
    driver_lib: Mapped[str] = mapped_column("driver_lib", String(50), comment="驱动库")
    connect_string_default: Mapped[str] = mapped_column("connect_string_default", String(500), comment="默认连接字符串")
    delete_status: Mapped[int] = mapped_column("delete_status", Boolean, comment="是否删除", default=0,
                                               nullable=True)


class DkDataSourcesInfo(DBBaseModel):
    __tablename__ = 'dk_datasource_info'
    datasource_type_id: Mapped[str] = mapped_column("datasource_type_id", comment="数据源类型ID")
    datasource_name: Mapped[str] = mapped_column("datasource_name", String(255), comment="数据源名称")
    host: Mapped[str] = mapped_column("host", String(100), comment="数据源主机IP")
    user_name: Mapped[str] = mapped_column("user_name", String(255), comment="用户名")
    password: Mapped[str] = mapped_column("password", String(255), comment="密码")
    connect_string: Mapped[str] = mapped_column("connect_string", String(500), comment="连接字符串")
    driver_name: Mapped[str] = mapped_column("driver_name", String(500), comment="驱动名称")
    default_db: Mapped[str] = mapped_column("default_db", String(255), comment="默认连接库名")
    driver_file_path: Mapped[str] = mapped_column("driver_file_path", String(500), comment="驱动绝对路径")
    port: Mapped[int] = mapped_column("port", Integer, comment="端口")
    creator: Mapped[str] = mapped_column("creator", String(255), comment="创建者")
    create_time: Mapped[DateTime] = mapped_column("create_time", DateTime, server_default=func.now(),
                                                  comment="创建时间")
    last_modifier: Mapped[str] = mapped_column("last_modifier", String(255), comment="上次修改用户")
    last_modify_time: Mapped[DateTime] = mapped_column("last_modify_time", DateTime, server_default=func.now(),
                                                       onupdate=func.now(),
                                                       comment="上次修改时间")