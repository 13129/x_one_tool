from enum import Enum
from typing import Optional, List, Union, Sequence, Dict, Type, Callable, Any, TypeVar

from fastapi import routing, params
from fastapi.datastructures import Default
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.utils import generate_unique_id
from pydantic import BaseModel

from apps.base import DEPENDENCIES

T = TypeVar("T", bound=BaseModel)


def MemoryAPIRouter(
        schema: Type[T] = None,
        prefix: str = "",
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[APIRoute]] = None,
        routes: Optional[List[routing.BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[Callable] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[APIRoute] = APIRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        get_all_route: Union[bool, DEPENDENCIES] = False,
        get_one_route: Union[bool, DEPENDENCIES] = False,
        create_route: Union[bool, DEPENDENCIES] = False,
        update_route: Union[bool, DEPENDENCIES] = False,
        delete_one_route: Union[bool, DEPENDENCIES] = False,
        delete_all_route: Union[bool, DEPENDENCIES] = False,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        )):
    def back(cls):
        cls.schema = schema
        cls.prefix = prefix  # 给类添加属性
        cls.tags = tags  # 给类添加属性
        cls.redirect_slashes = redirect_slashes  # 给类添加属性
        cls.deprecated = deprecated  # 给类添加属性
        cls.include_in_schema = include_in_schema  # 给类添加属性
        cls.dependencies = dependencies  # 给类添加属性
        cls.default_response_class = default_response_class  # 给类添加属性
        cls.responses = responses  # 给类添加属性
        cls.callbacks = callbacks  # 给类添加属性
        cls.routes = routes  # 给类添加属性
        cls.default = default  # 给类添加属性
        cls.dependency_overrides_provider = dependency_overrides_provider  # 给类添加属性
        cls.route_class = route_class  # 给类添加属性
        cls.on_startup = on_startup  # 给类添加属性
        cls.on_shutdown = on_shutdown  # 给类添加属性
        cls.generate_unique_id_function = generate_unique_id_function  # 给类添加属性
        cls.get_all_route = get_all_route
        cls.get_one_route = get_one_route
        cls.create_route = create_route
        cls.update_route = update_route
        cls.delete_one_route = delete_one_route
        cls.delete_all_route = delete_all_route

        return cls

    return back
