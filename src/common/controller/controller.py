import abc
import functools
import inspect
from enum import Enum
from typing import Any, List, Optional, Union

from fastapi.datastructures import Default
from fastapi.responses import JSONResponse
from fastapi.utils import generate_unique_id
from sqlalchemy.orm import Session

from src.common.middleware.router_class import ContextIncludedRoute
from src.core import RouteArgsBase
from src.core.container import BaseContainer
from xlogger import Logger
from .crud import VCRUDRouterBase


class VControllerBase(metaclass=abc.ABCMeta):
    __slots__ = ["api_router", "tags", "prefix", "session"]
    prefix: Optional[str]
    tags: Optional[List[Union[str, Enum]]]
    session: Optional[Session]
    logger: Logger = BaseContainer.logger().xlog

    def __init__(self):
        self.api_router = None

    @property
    def cls(self):
        return type(self)

    @property
    def this_router_api(self):
        return self.api_router

    def _creat_api_router(self) -> VCRUDRouterBase:
        if not self.api_router:
            self.api_router = VCRUDRouterBase(
                prefix=getattr(self.cls, 'prefix', None),
                tags=getattr(self.cls, 'tags', None),
                dependencies=getattr(self.cls, 'dependencies', None),
                default_response_class=getattr(self.cls, 'default_response_class', Default(JSONResponse)),
                responses=getattr(self.cls, 'responses', None),
                callbacks=getattr(self.cls, 'callbacks', None),
                routes=getattr(self.cls, 'routes', None),
                redirect_slashes=getattr(self.cls, 'redirect_slashes', True),
                default=getattr(self.cls, 'default', None),
                dependency_overrides_provider=getattr(self.cls, 'dependency_overrides_provider', None),
                route_class=getattr(self.cls, 'route_class', ContextIncludedRoute),
                on_startup=getattr(self.cls, 'on_startup', None),
                on_shutdown=getattr(self.cls, 'on_shutdown', None),
                deprecated=getattr(self.cls, 'deprecated', None),
                include_in_schema=getattr(self.cls, 'include_in_schema', True),
                generate_unique_id_function=getattr(self.cls, 'generate_unique_id_function',
                                                    Default(generate_unique_id)),
            )

        return self.api_router

    def _register_endpoint(self) -> VCRUDRouterBase:
        # 获取当前注入的APIRouter对象
        assert hasattr(self, 'api_router'), '需要实例化APIRouter对象'
        # 获取当前注入的APIRouter对象
        self._creat_api_router()
        # 当前类下下定义对应的特定特点包含有被标记了_endpoint属性的路由函数
        for i in dir(self.cls):
            # 获取到注册到函数中的对应_endpoint函数对象
            route_endpoint = getattr(self.cls, i)
            # 判断是否是被RestRout给注册的端点函数
            if (inspect.isfunction(route_endpoint) or inspect.iscoroutinefunction(route_endpoint)) and hasattr(
                    route_endpoint, '_route_endpoint'):
                # 如果是指定的端点函数对象，透传当前self到当前的函数中
                # 要获取到对应的_endpoint绑定的函数，不能直接的获取getattr(self.cls, i)，不然会出现丢失__name__问题
                route_endpoint = getattr(route_endpoint, '_route_endpoint')
                # 路由参数对象信息
                route_args: RouteArgsBase = getattr(route_endpoint, '_route_args')
                # 传递self对象到对应_endpoint函数对象
                curr_route_endpoint = functools.partial(route_endpoint, self)
                # 注意事项---处理经过functools.partial后丢失__name__的问题
                route_args.name = route_args.name or route_endpoint.__name__

                def cleandoc():
                    curr_route_endpoint.__doc__ = ''

                # 函数注释说明信息。文档显示描述问题处理
                route_args.description = route_args.description or inspect.cleandoc(
                    route_endpoint.__doc__ or '') or cleandoc()
                # 开始添加当前被被RestRout给注册的端点函数
                self.api_router.add_api_route(**route_args.model_dump(), endpoint=curr_route_endpoint)
        return self.api_router

    def build(self) -> VCRUDRouterBase:
        #  注册点点路由
        return self._register_endpoint()

    @classmethod
    def instance(cls) -> VCRUDRouterBase:
        """实例化"""
        return cls().build()
