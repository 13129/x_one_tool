"""
coding:utf-8
@Time:2022/8/4 23:11
@Author:XJC
@Description:
"""

import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import as_declarative, declared_attr


def uuid_hex():
    return str(uuid.uuid4().hex)


@as_declarative()
class DBBaseModel:
    id = Column(String(64), primary_key=True, default=uuid_hex)

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
