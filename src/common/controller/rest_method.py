from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Type, Union

from fastapi import params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute

from src.core.schema import RouteArgsBase


def rest_route_decorator(methods_default: Optional[Union[Set[str], List[str]]]):
    def decorator(path: str,
                  methods=None,
                  response_model: Optional[Type[Any]] = None,
                  status_code: Optional[int] = None,
                  tags: Optional[List[Union[str, Enum]]] = None,
                  dependencies: Optional[Sequence[params.Depends]] = None,
                  summary: Optional[str] = None,
                  description: Optional[str] = None,
                  response_description: str = "Successful Response",
                  responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
                  deprecated: Optional[bool] = None,
                  operation_id: Optional[str] = None,
                  response_model_include: Optional[Union[Set, Dict]] = None,
                  response_model_exclude: Optional[Union[Set, Dict]] = None,
                  response_model_by_alias: bool = True,
                  response_model_exclude_unset: bool = False,
                  response_model_exclude_defaults: bool = False,
                  response_model_exclude_none: bool = False,
                  include_in_schema: bool = True,
                  response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
                  name: Optional[str] = None,
                  callbacks: Optional[List[APIRoute]] = None,
                  openapi_extra: Optional[Dict[str, Any]] = None,
                  **kwargs: Any):
        if methods is None:
            methods = methods_default

        def call_func(fun: Callable) -> Callable[[Callable], Callable]:
            route_args = RouteArgsBase(path=path,
                                       name=name,
                                       status_code=status_code,
                                       methods=methods,
                                       tags=tags,
                                       dependencies=dependencies,
                                       description=description,
                                       summary=summary,
                                       response_description=response_description,
                                       responses=responses,
                                       deprecated=deprecated,
                                       operation_id=operation_id,
                                       response_model_include=response_model_include,
                                       response_model_exclude=response_model_exclude,
                                       response_model_by_alias=response_model_by_alias,
                                       response_model_exclude_unset=response_model_exclude_unset,
                                       response_model_exclude_defaults=response_model_exclude_defaults,
                                       response_model_exclude_none=response_model_exclude_none,
                                       include_in_schema=include_in_schema,
                                       response_class=response_class,
                                       callbacks=callbacks,
                                       openapi_extra=openapi_extra,
                                       response_model=response_model,
                                       **kwargs)

            setattr(fun, '_route_args', route_args)
            setattr(fun, '_route_endpoint', fun)
            return fun

        return call_func

    return decorator
