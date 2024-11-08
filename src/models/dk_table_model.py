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

class DkTableInfo(DBBaseModel):
    __tablename__ = 'dk_catalog_table'
    datasource_id = Column("datasource_id", String(255), comment="数据源ID")
    name = Column("name", String(128), comment="表中文名")
    physical_table_name = Column("physical_table_name", String(128), comment="物理表名")
    logic_table_name = Column("logic_table_name", String(128), comment="逻辑表名")
    table_name_alias = Column("table_name_alias", String(255), comment="表中文别名")
    table_code = Column("table_code", Integer, comment="表编码")
    table_type = Column("table_type", String(64), comment="表类型")
    is_open = Column("is_open", Boolean, default=True, comment="是否公开;1-公开;0不公开")
    is_edit = Column("is_edit", Boolean, default=False, comment="是否可编辑;1-可编辑;0不可编辑")
    order_no = Column("order_no", Integer, comment="排序")
    creator = Column("creator", String(255), comment="创建者")
    create_time = Column("create_time", DateTime, server_default=func.now(), comment="创建时间")
    last_modifier = Column("last_modifier", String(255), comment="上次修改用户")
    last_modify_time = Column("last_modify_time", DateTime, server_default=func.now(), onupdate=func.now(),
                              comment="上次修改时间")

    fields = relationship(
        'DkTableFieldInfo',
        primaryjoin='DkTableInfo.table_code==foreign(DkTableFieldInfo.table_code)',
        backref=backref('dk_catalog_table')
    )


class DkTableFieldInfo(DBBaseModel):
    __tablename__ = 'dk_catalog_field'
    table_code = Column("table_code", Integer, comment="表编码")
    physical_table_name = Column("physical_table_name", String(128), comment="物理表名")
    name_en = Column("name_en", String(128), comment="字段英文名")
    name_cn = Column("name_cn", String(512), comment="字段中文名")
    is_pk = Column("is_pk", Boolean, default=False, comment="是否主键:1:是;0:否")
    is_show_list = Column("is_show_list", Boolean, default=False, comment="是否在列表显示")
    is_show_detail = Column("is_show_detail", Boolean, default=False, comment="是否在详情显示")
    order_no = Column("order_no", Integer, comment="排序")
    type = Column("type", String(128), comment="字段类型")
    domain_value = Column("domain_value", Text, comment="域值")
    is_image = Column("is_image", Boolean, default=False, comment="是否以图片展示1:是;0:否")
    creator = Column("creator", String(255), comment="创建者")
    create_time = Column("create_time", DateTime, server_default=func.now(), comment="创建时间")
    last_modifier = Column("last_modifier", String(255), comment="上次修改用户")
    last_modify_time = Column("last_modify_time", DateTime, server_default=func.now(), onupdate=func.now(),
                              comment="上次修改时间")
