"""
coding:utf-8
@Time:2022/8/4 23:11
@Author:XJC
@Description:
"""

import uuid

from sqlalchemy import String
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, mapped_column


def uuid_hex():
    return str(uuid.uuid4().hex)


@as_declarative()
class DBBaseModel:
    id:Mapped[str] = mapped_column(String(64), primary_key=True, default=uuid_hex)
