import abc
import functools
import inspect

from apps.common.memory_crud import MemoryCRUDRouter


class RouteArgs:
    def dict(self):
        pass


class IBaseController(metaclass=abc.ABCMeta):

    def __init__(self):
        self.api_router = None

    @property
    def cls(self):
        return type(self)

    @property
    def this_router_api(self):
        return self.api_router

    def _creat_api_router(self) -> MemoryCRUDRouter:
        pass
        if not self.api_router:
            pass
            self.api_router = MemoryCRUDRouter(
                schema=getattr(self.cls, 'schema'),
                prefix=getattr(self.cls, 'prefix'),
                tags=getattr(self.cls, 'tags'),
                dependencies=getattr(self.cls, 'dependencies'),
                default_response_class=getattr(self.cls, 'default_response_class'),
                responses=getattr(self.cls, 'responses'),
                callbacks=getattr(self.cls, 'callbacks'),
                routes=getattr(self.cls, 'routes'),
                redirect_slashes=getattr(self.cls, 'redirect_slashes'),
                default=getattr(self.cls, 'default'),
                dependency_overrides_provider=getattr(self.cls, 'dependency_overrides_provider'),
                route_class=getattr(self.cls, 'route_class'),
                on_startup=getattr(self.cls, 'on_startup'),
                on_shutdown=getattr(self.cls, 'on_shutdown'),
                deprecated=getattr(self.cls, 'deprecated'),
                include_in_schema=getattr(self.cls, 'include_in_schema'),
                generate_unique_id_function=getattr(self.cls, 'generate_unique_id_function'),
                get_all_route=getattr(self.cls, 'get_all_route', False),
                get_one_route=getattr(self.cls, 'get_one_route', False),
                create_route=getattr(self.cls, 'create_route', False),
                update_route=getattr(self.cls, 'update_route', False),
                delete_one_route=getattr(self.cls, 'delete_one_route', False),
                delete_all_route=getattr(self.cls, 'delete_all_route', False),
            )

        return self.api_router

    def _register_endpoint(self) -> MemoryCRUDRouter:
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
                # route_args: RouteArgs = getattr(route_endpoint, '_route_args')
                route_args = getattr(route_endpoint, '_route_args')
                # 传递self对象到对应_endpoint函数对象
                curr_route_endpoint = functools.partial(route_endpoint, self)
                # 注意事项---处理经过functools.partial后丢失__name__的问题
                # setattr(curr_route_endpoint, '__name__', route_endpoint.__name__)
                route_args.name = route_args.name or route_endpoint.__name__

                def cleandoc():
                    curr_route_endpoint.__doc__ = ''

                # 函数注释说明信息。文档显示描述问题处理
                route_args.description = route_args.description or inspect.cleandoc(
                    route_endpoint.__doc__ or '') or cleandoc()
                # 开始添加当前被被RestRout给注册的端点函数
                self.api_router.add_api_route(**route_args.dict(),
                                              endpoint=curr_route_endpoint)
        return self.api_router

    def build(self) -> MemoryCRUDRouter:
        #  注册点点路由
        return self._register_endpoint()

    @classmethod
    def instance(cls) -> MemoryCRUDRouter:
        """实例化"""
        return cls().build()
