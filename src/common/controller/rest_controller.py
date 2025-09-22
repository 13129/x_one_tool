#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName    : rest_controller.py
@Time    : 2025/8/2 22:37
@Author  : XJC
@Description: 
"""
# src/core/decorators/controller.py
from typing import Optional, List, Union, Sequence, Type
from enum import Enum
from fastapi.params import Depends
from src.core.schema import RouteArgsBase


def api_controller(
        prefix: Optional[str] = "",
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        permissions: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        enable_logging: bool = True,
        include_in_schema: bool = True,
        **kwargs  # 其他可传递给路由的参数
):
    """
    类装饰器：用于标记控制器类，并设置默认配置
    """

    def decorator(cls: Type) -> Type:
        # 设置类属性
        if prefix is not None:
            cls.prefix = prefix
        if tags is not None:
            cls.tags = tags
        if dependencies is not None:
            cls.dependencies = dependencies
        if permissions is not None:
            cls.permissions = permissions
        if roles is not None:
            cls.roles = roles
        cls.enable_logging = enable_logging
        cls.include_in_schema = include_in_schema

        # 传递其他参数
        for k, v in kwargs.items():
            setattr(cls, k, v)

        # 标记为控制器类
        cls._is_api_controller = True

        return cls

    return decorator
