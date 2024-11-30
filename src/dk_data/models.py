#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :models.py
@Time      :2024/11/29 14:11
@Author    :XJC
@Description:
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from src.core import DBBaseModel


class DkDataSourcesType(DBBaseModel):
    __tablename__ = 'dk_datasource_type'
    type_name: Mapped[str] = mapped_column(String(50), comment="数据源类型名称")
    is_async: Mapped[int] = mapped_column(Boolean, comment="是否异步", default=0)
    driver_lib: Mapped[str] = mapped_column(String(50), comment="驱动库")
    connect_string_default: Mapped[str] = mapped_column(String(500), comment="默认连接字符串")
    delete_status: Mapped[int] = mapped_column(Boolean, comment="是否删除", default=0,
                                               nullable=True)


class DkDataSourcesInfo(DBBaseModel):
    __tablename__ = 'dk_datasource_info'
    datasource_type_id: Mapped[str] = mapped_column(comment="数据源类型ID")
    datasource_name: Mapped[str] = mapped_column(String(255), comment="数据源名称")
    host: Mapped[str] = mapped_column(String(100), comment="数据源主机IP")
    user_name: Mapped[Optional[str]] = mapped_column(String(255), comment="用户名")
    password: Mapped[Optional[str]] = mapped_column(String(255), comment="密码")
    connect_string: Mapped[str] = mapped_column(String(500), comment="连接字符串")
    driver_name: Mapped[str] = mapped_column(String(500), comment="驱动名称")
    default_db: Mapped[str] = mapped_column(String(255), comment="默认连接库名")
    driver_file_path: Mapped[str] = mapped_column(String(500), comment="驱动绝对路径")
    port: Mapped[int] = mapped_column(Integer, comment="端口")
    creator: Mapped[Optional[str]] = mapped_column(String(255), comment="创建者")
    create_time: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(),
                                                  comment="创建时间")
    last_modifier: Mapped[Optional[str]] = mapped_column(String(255), comment="上次修改用户")
    last_modify_time: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(),
                                                       onupdate=func.now(),
                                                       comment="上次修改时间")


class DkTableInfo(DBBaseModel):
    __tablename__ = 'dk_catalog_table'
    datasource_id: Mapped[str] = Column(String(255), comment="数据源ID")
    name: Mapped[Optional[str]] = Column(String(128), comment="表中文名")
    physical_table_name: Mapped[str] = Column(String(128), comment="物理表名")
    logic_table_name: Mapped[Optional[str]] = Column(String(128), comment="逻辑表名")
    table_name_alias: Mapped[Optional[str]] = Column(String(255), comment="表中文别名")
    table_code: Mapped[int] = Column(Integer, comment="表编码")
    table_type: Mapped[str] = Column(String(64), comment="表类型")
    is_open: Mapped[bool] = Column(Boolean, default=True, comment="是否公开;1-公开;0不公开")
    is_edit: Mapped[bool] = Column(Boolean, default=False, comment="是否可编辑;1-可编辑;0不可编辑")
    order_no: Mapped[int] = Column(Integer, comment="排序")
    creator: Mapped[Optional[str]] = Column(String(255), comment="创建者")
    create_time: Mapped[datetime] = Column(DateTime, server_default=func.now(), comment="创建时间")
    last_modifier: Mapped[Optional[str]] = Column(String(255), comment="上次修改用户")
    last_modify_time: Mapped[datetime] = Column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                comment="上次修改时间")

    fields = relationship(
        'DkTableFieldInfo',
        primaryjoin='DkTableInfo.table_code==foreign(DkTableFieldInfo.table_code)',
        backref=backref('dk_catalog_table')
    )


class DkTableFieldInfo(DBBaseModel):
    __tablename__ = 'dk_catalog_field'
    table_code: Mapped[str] = Column(Integer, comment="表编码")
    physical_table_name: Mapped[str] = Column(String(128), comment="物理表名")
    name_en: Mapped[str] = Column(String(128), comment="字段英文名")
    name_cn: Mapped[Optional[str]] = Column(String(512), comment="字段中文名")
    is_pk: Mapped[Optional[bool]] = Column(Boolean, default=False, comment="是否主键:1:是;0:否")
    is_show_list: Mapped[bool] = Column(Boolean, default=False, comment="是否在列表显示")
    is_show_detail: Mapped[bool] = Column(Boolean, default=False, comment="是否在详情显示")
    order_no: Mapped[int] = Column(Integer, comment="排序")
    type: Mapped[str] = Column(String(128), comment="字段类型")
    domain_value: Mapped[str] = Column(Text, comment="域值")
    is_image: Mapped[bool] = Column(Boolean, default=False, comment="是否以图片展示1:是;0:否")
    creator: Mapped[Optional[str]] = Column(String(255), comment="创建者")
    create_time: Mapped[datetime] = Column(DateTime, server_default=func.now(), comment="创建时间")
    last_modifier: Mapped[Optional[str]] = Column(String(255), comment="上次修改用户")
    last_modify_time: Mapped[datetime] = Column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                comment="上次修改时间")


class DkCatalog(DBBaseModel):
    __tablename__ = 'dk_catalog'
    name_cn: Mapped[Optional[str]] = mapped_column(String(128), comment="中文名")
    name_en: Mapped[str] = mapped_column(String(128), comment="英文名")
    catalog_code: Mapped[str] = mapped_column(String(128), comment="目录编码")
    parent_id: Mapped[str] = mapped_column(String(255), comment="父级")
    order_no: Mapped[int] = mapped_column(Integer, comment="排序")
    is_show: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否显示:1显示;0不显示")
    creator: Mapped[Optional[str]] = mapped_column(String(255), comment="创建者")
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    last_modifier: Mapped[Optional[str]] = mapped_column(String(255), comment="上次修改用户")
    last_modify_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                       comment="上次修改时间")


class DkCatalogTableRelational(DBBaseModel):
    __tablename__ = 'dk_catalog_table_relational_info'
    catalog_code_id: Mapped[str] = Column(String(128), comment="目录编码ID")
    tabl_code_id: Mapped[str] = Column(String(128), comment="表编码ID")
    order_no: Mapped[int] = Column(Integer, comment="排序")
    is_show: Mapped[bool] = Column(Boolean, default=True, comment="是否显示:1显示;0不显示")
    creator: Mapped[Optional[str]] = Column(String(255), comment="创建者")
    create_time: Mapped[datetime] = Column(DateTime, server_default=func.now(), comment="创建时间")
    last_modifier: Mapped[Optional[str]] = Column(String(255), comment="上次修改用户")
    last_modify_time: Mapped[datetime] = Column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                comment="上次修改时间")
