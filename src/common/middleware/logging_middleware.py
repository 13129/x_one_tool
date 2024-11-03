#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName    : logging_middleware.py
@Time    : 2024/11/3 12:59
@Author  : XJC
@Description: 
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import Message


# class LoggingMiddleware(BaseHTTPMiddleware):
#
#     def __init__(self, app):
#         super().__init__(app)
#
#     async def set_body(self, request: Request):
#         receive_ = await request._receive()
#
#         async def receive() -> Message:
#             return receive_
#
#         request._receive = receive
#
#     async def dispatch(self, request, call_next):
#         await self.set_body(request)

        # body = await request.body()
        # json_body = await request

        # print(body)
        # print(json_body)
        #
        # response = await call_next(request)
        #
        # return response
