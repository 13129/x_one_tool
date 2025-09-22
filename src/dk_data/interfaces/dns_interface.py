#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName    : dns_interface.py
@Time    : 2025/8/2 23:42
@Author  : XJC
@Description: 
"""
# src/dk_data/interfaces.py
from typing import Protocol, List, Any
from typing_extensions import runtime_checkable


@runtime_checkable
class DnsServiceInterface(Protocol):
    async def get_all(self) -> List[Any]:
        pass

    async def get_one(self, _id: str) -> Any:
        pass

    async def delete(self, _id: str) -> Any:
        pass
