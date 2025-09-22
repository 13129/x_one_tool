from enum import Enum
from typing import Any, Dict, List, Sequence, Set, Type, Union
from typing import Generic, Optional, TypeVar, Callable

from fastapi import params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel

T = TypeVar('T')  # 泛型类型 T


class ResultJson(BaseModel, Generic[T]):
    code: Optional[int] = 200
    message: Optional[str] = 'Success'
    data: Optional[T] = None


class BaseModelSchema(BaseModel):
    id: Union[str, None]

    class Config:
        orm = False


class RouteArgsBase(BaseModel):
    path: str
    response_model: Optional[Type[Any]] = None
    status_code: Optional[int] = None
    tags: Optional[List[Union[str, Enum]]] = None
    dependencies: Optional[Sequence[params.Depends]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    response_description: str = "Successful Response"
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    deprecated: Optional[bool] = None
    methods: Optional[Union[Set[str], List[str]]] = None
    operation_id: Optional[str] = None
    response_model_include: Optional[Union[Set, Dict]] = None
    response_model_exclude: Optional[Union[Set, Dict]] = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    include_in_schema: bool = True
    response_class: Union[Type[Response], DefaultPlaceholder] = Default(
        JSONResponse
    )
    name: Optional[str] = None
    route_class_override: Optional[Type[APIRoute]] = None
    callbacks: Optional[List[APIRoute]] = None
    openapi_extra: Optional[Dict[str, Any]] = None

    # 权限控制扩展字段（自定义）
    # permissions: Optional[List[str]] = None  # 如 ["user:read", "admin"]
    # roles: Optional[List[str]] = None  # 如 ["admin", "editor"]
    # scopes: Optional[List[str]] = None  # OAuth2 scopes
    #
    # # 日志标记
    # enable_logging: bool = True
    # log_request: bool = True
    # log_response: bool = True
    #
    # # 自定义中间件钩子
    # pre_handler: Optional[Callable] = None  # 执行前
    # post_handler: Optional[Callable] = None  # 成功后
    # on_error: Optional[Callable] = None  # 出错时

    class Config:
        arbitrary_types_allowed = True
        # extra = "allow"  # 允许额外字段（兼容未来 FastAPI 更新）
