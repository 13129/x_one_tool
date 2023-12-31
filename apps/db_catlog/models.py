"""
coding:utf-8
@Time:2022/8/4 23:10
@Author:XJC
@Description:
"""
from sqlalchemy import Column, String, DateTime, Boolean, func, Integer, Text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref, declared_attr, declarative_mixin, Relationship

from apps.base import DBBaseModel


@declarative_mixin
class DnsInfoRefTargetMixin:
    @declared_attr
    def datasource_type_info(self):
        return relationship('DkDNSType',
                            primaryjoin="DkDNSType.id==foreign(%s.datasource_type_id)" % self.__name__,
                            backref=backref('dk_datasource_info')
                            )


@declarative_mixin
class CatalogTableRefTargetMixin:
    @declared_attr
    def datasource_info(self):
        return relationship('DkDnsInfo',
                            primaryjoin='DkDnsInfo.id==foreign(%s.datasource_id) ' % self.__name__,
                            backref=backref('dk_catalog_table'))

    @declared_attr
    def field_info(self):
        return relationship('DkCatalogField',
                            primaryjoin='DkCatalogTable.table_code==foreign(DkCatalogField.table_code)',
                            backref=backref('dk_catalog_table'))

    @declared_attr
    def catalog_info_proxy(self):
        return association_proxy("ctl_tb_relation_info", "catalog_info")


@declarative_mixin
class CatalogRefTargetMixin:
    @declared_attr
    def child_info(self):
        return relationship("DkCatalog",
                            primaryjoin='DkCatalog.id==foreign(DkCatalog.parent_id)',
                            backref=backref('dk_catalog', remote_side='DkCatalog.id'))

    @declared_attr
    def table_info_proxy(self):
        return association_proxy("ctl_tb_relation_info", "table_info")


@declarative_mixin
class CatalogTableRRefTargetMixin:
    @declared_attr
    def catalog_info(self):
        return relationship("DkCatalog",
                            primaryjoin='foreign(dk_catalog_table_relational_info.c.catalog_code_id)==DkCatalog.id',
                            backref=backref("ctl_tb_relation_info"))

    @declared_attr
    def table_info(self):
        return relationship("DkCatalogTable",
                            primaryjoin='foreign(dk_catalog_table_relational_info.c.tabl_code_id)==DkCatalogTable.id',
                            backref=backref('ctl_tb_relation_info'))


class DkDNSType(DBBaseModel):
    __tablename__ = 'dk_datasource_type'
    type_name = Column("type_name", String(50), comment="数据源类型名称")
    is_async = Column("is_async", Boolean, default=False, comment="是否异步")
    driver_lib = Column("driver_lib", String(50), comment="驱动库")
    connect_string_default = Column("connect_string_default", String(500), comment="默认连接字符串")
    delete_status = Column("delete_status", Boolean, comment="是否删除", default='True', nullable=True)


class DkDnsInfo(DBBaseModel, DnsInfoRefTargetMixin):
    __tablename__ = 'dk_datasource_info'
    datasource_type_id = Column("datasource_type_id", String(50), comment="数据源类型ID")
    datasource_name = Column("datasource_name", String(255), comment="数据源名称")
    host = Column("host", String(100), comment="数据源主机IP")
    user_name = Column("user_name", String(255), comment="用户名")
    password = Column("password", String(255), comment="密码")
    connect_string = Column("connect_string", String(500), comment="连接字符串")
    driver_name = Column("driver_name", String(500), comment="驱动名称")
    default_db = Column("default_db", String(255), comment="默认连接库名")
    driver_file_path = Column("driver_file_path", String(500), comment="驱动绝对路径")
    port = Column("port", Integer, comment="端口")
    creator = Column("creator", String(255), comment="创建者")
    create_time = Column("create_time", DateTime, server_default=func.now(), comment="创建时间")
    last_modifier = Column("last_modifier", String(255), comment="上次修改用户")
    last_modify_time = Column("last_modify_time", DateTime, server_default=func.now(), onupdate=func.now(),
                              comment="上次修改时间")


class DkCatalogTable(DBBaseModel, CatalogTableRefTargetMixin):
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


class DkCatalogField(DBBaseModel):
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


class DkCatalog(DBBaseModel, CatalogRefTargetMixin):
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


class DkCatalogTableRelational(DBBaseModel, CatalogTableRRefTargetMixin):
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
