from typing import Generic, Optional, TypeVar
from typing import Type, Any, List, Sequence, Dict, Union, Set

from fastapi import params
from fastapi.datastructures import DefaultPlaceholder, Default
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel, model_validator

T = TypeVar('T')  # 泛型类型 T


class ResultJson(BaseModel, Generic[T]):
    code: int = 200
    message: str = 'Success'
    data: Optional[T] = None


class BaseModelSchema(BaseModel):
    id: Union[str, None]

    class Config:
        orm = False


class RouteArgsBase(BaseModel):
    path: str
    response_model: Optional[Type[Any]] = None
    status_code: Optional[int] = None
    tags: Optional[List[str]] = None
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

    class Config:
        arbitrary_types_allowed = True


