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

class DkCatalog(DBBaseModel):
    __tablename__ = 'dk_catalog'
    name_cn = Column("name_cn", String(128), comment="中文名")
    name_en = Column("name_en", String(128), comment="英文名")
    catalog_code = Column("catalog_code", String(128), comment="目录编码")
    parent_id = Column("parent_id", String(255), comment="父级")
    order_no = Column("order_no", Integer, comment="排序")
    is_show = Column("is_show", Boolean, default=True, comment="是否显示:1显示;0不显示")
    creator = Column("creator", String(255), comment="创建者")
    create_time = Column("create_time", DateTime, server_default=func.now(), comment="创建时间")
    last_modifier = Column("last_modifier", String(255), comment="上次修改用户")
    last_modify_time = Column("last_modify_time", DateTime, server_default=func.now(), onupdate=func.now(),
                              comment="上次修改时间")


class DkCatalogTableRelational(DBBaseModel):
    __tablename__ = 'dk_catalog_table_relational_info'
    catalog_code_id = Column("catalog_code_id", String(128), comment="目录编码ID")
    tabl_code_id = Column("tabl_code_id", String(128), comment="表编码ID")
    order_no = Column("order_no", Integer, comment="排序")
    is_show = Column("is_show", Boolean, default=True, comment="是否显示:1显示;0不显示")
    creator = Column("creator", String(255), comment="创建者")
    create_time = Column("create_time", DateTime, server_default=func.now(), comment="创建时间")
    last_modifier = Column("last_modifier", String(255), comment="上次修改用户")
    last_modify_time = Column("last_modify_time", DateTime, server_default=func.now(), onupdate=func.now(),
                              comment="上次修改时间")