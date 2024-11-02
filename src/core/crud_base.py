"""
coding:utf-8
@Time:2022/8/4 23:24
@Author:XJC
@Description:
"""
from abc import ABC
from typing import Any, Callable, Generic, List, Optional, Type, Union

from fastapi import APIRouter, HTTPException
from fastapi.types import DecoratedCallable

from .types import T, DEPENDENCIES

NOT_FOUND = HTTPException(404, "Item not found")


class CRUDGenerator(Generic[T], APIRouter, ABC):
    schema: Type[T]
    _base_path: str = "/"

    def __init__(
            self,
            prefix: Optional[str] = None,
            tags: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> None:

        prefix = str(prefix if prefix else self.schema.__name__)
        prefix = self._base_path + prefix.strip("/")
        tags = tags or [prefix.strip("/").capitalize()]

        super().__init__(prefix=prefix, tags=tags, **kwargs)

    def _add_api_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            dependencies: Union[bool, DEPENDENCIES],
            error_responses: Optional[List[HTTPException]] = None,
            **kwargs: Any,
    ) -> None:
        dependencies = [] if isinstance(dependencies, bool) else dependencies
        responses: Any = (
            {err.status_code: {"detail": err.detail} for err in error_responses}
            if error_responses
            else None
        )

        super().add_api_route(
            path, endpoint, dependencies=dependencies, responses=responses, **kwargs
        )

    def api_route(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Overrides and exiting route if it exists"""
        methods = kwargs["methods"] if "methods" in kwargs else ["GET"]
        self.remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def get(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["Get"])
        return super().get(path, *args, **kwargs)

    def post(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        methods_ = set(methods)

        for route in self.routes:
            if (
                    route.path == f"{self.prefix}{path}"  # type: ignore
                    and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    def _raise(self, e: Exception, status_code: int = 422) -> HTTPException:
        raise HTTPException(422, ", ".join(e.args)) from e
