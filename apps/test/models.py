from enum import Enum

from fastapi import APIRouter
from pydantic import Field, BaseModel
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Enum as EnumType
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy_json import NestedMutableJson, MutableJson

from apps.base import DBBaseModel
from apps.common import SQLAlchemyCRUDRouter as CRUDRouter
from apps.db import get_db


# 定义枚举类型
class StatusEnum(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class DbTestModel(DBBaseModel):
    __tablename__ = 'db_test'
    type_name: Mapped[str] = mapped_column(name="type_name", type_=String(50), comment="数据源类型名称")
    connect_string_default: Mapped[str] = mapped_column(name="connect_string_default", type_=String(500),
                                                        comment="默认连接字符串")
    delete_status: Mapped[bool] = mapped_column(name="delete_status", type_=Boolean, comment="默认连接", default='False',
                                                nullable=True)
    status: Mapped[str] = mapped_column(EnumType(StatusEnum))
    status2: Mapped[str] = mapped_column(MutableJson)


class DbTestSchema(BaseModel):
    type_name: str
    connect_string_default: str
    delete_status: bool = Field(default=True)
    status: str
    status2: str

    class Config:
        from_attributes = True


class DbTestSchemaCreate(DBBaseModel):
    # type_name: str
    connect_string_default: str
    delete_status: bool = Field(default=True)
    status: str

    # status2: str

    class Config:
        from_attributes = True


class DbTestRouter:
    """
    用于管理数据源驱动的增删改查
    """
    router = CRUDRouter(schema=DbTestSchema, create_schema=DbTestSchemaCreate, db_model=DbTestModel,
                        db=get_db,
                        tags=["测试数据"], prefix='db_test')


router = APIRouter()
router.include_router(DbTestRouter.router)
test_api = APIRouter()
test_api.include_router(router, prefix="/test", )
