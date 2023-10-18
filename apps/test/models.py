from enum import Enum
from fastapi import Depends, Query
from pydantic import BaseModel
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from apps.base import DBBaseModel
from fastapi_pagination import LimitOffsetPage, Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from apps.common import SQLAlchemyCRUDRouter as CRUDRouter
from apps.db import get_db
from sqlalchemy import select


# 定义枚举类型
class StatusEnum(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class DbTestSchema(BaseModel):
    type_name: str
    connect_string_default: str
    delete_status: bool

    class Config:
        from_attributes = True


class DbTestModel(DBBaseModel):
    __tablename__ = 'db_test'
    __pydantic_model__ = DbTestSchema
    type_name = Column(String(64), default=None, comment="数据源类型名称")
    connect_string_default = Column(String(500), default=None, comment="默认连接字符串")
    delete_status = Column(Boolean, default=False, comment="默认连接", nullable=True)


class DbTestRouter:
    """
    用于管理数据源驱动的增删改查
    """
    router = CRUDRouter(schema=DbTestSchema, db_model=DbTestModel,
                        db=get_db,
                        update_route=False, delete_all_route=False, delete_one_route=False, get_all_route=False,
                        tags=["性能测试"], prefix='DbTest')

    @staticmethod
    @router.api_route('/queryDataGetLimit/', methods=['GET'], summary='性能测试LimitOffsetPage',
                      response_model=LimitOffsetPage[router.schema])
    async def overloaded_dk_dns_type_get_all(session=Depends(router.db_func)):
        query = select(DbTestModel).order_by(DbTestModel.id)
        return await paginate(session, query)

    @staticmethod
    @router.api_route('/queryDataPage/', methods=['GET'], summary='性能测试Page', response_model=Page[router.schema])
    async def overloaded_dk_dns_type_get_all(session=Depends(router.db_func)):
        query = select(DbTestModel).order_by(DbTestModel.id)
        return await paginate(session, query)
