from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from apps.base import BaseModel


# @as_declarative()
class DbTestModel(BaseModel):
    __tablename__ = 'db_test'
    # id = Column(String(64), primary_key=True, autoincrement=True)
    type_name = Column("type_name", String(50), comment="数据源类型名称")
    connect_string_default = Column("connect_string_default", String(500), comment="默认连接字符串")
    delete_status = Column("delete_status", Boolean, comment="默认连接字符串", default='False', nullable=True)
