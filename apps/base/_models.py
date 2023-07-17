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


@as_declarative()
class BaseModel:
    id = Column(String(64), primary_key=True, default=str(uuid.uuid4()))
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
