# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :router_class.py
@Time      :2024/1/5 18:29
@Author    :XJC
@Description:
"""
import uuid
from json import JSONDecodeError
from time import perf_counter
from typing import Callable

from fastapi import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute

from xlogger import log as loggers
from .json_dp import dict_to_json_ensure_ascii, json_to_dict


class ContextIncludedRoute(APIRoute):

    @staticmethod
    async def async_trace_add_log_record(request: Request, event_des: str = None, msg_dict: dict = None,
                                         remarks: str = None):
        """
        :param request:
        :param event_des: 日志记录事件描述
        :param msg_dict: 日志记录信息字典
        :param remarks: 日志备注信息
        :return:
        """

        if hasattr(request, 'traceid'):
            log = {
                'traceid': getattr(request, 'traceid'),
                'trace_index': getattr(request, 'trace_links_index'),
                'event_des': event_des,
                'msg_dict': msg_dict,
                'remarks': remarks
            }
            if not remarks:
                log.pop('remarks')
            if not msg_dict:
                log.pop('msg_dict')
            try:
                log_msg = dict_to_json_ensure_ascii(log)
                loggers.info(log_msg)
            except:
                loggers.info(
                    getattr(request, 'traceid') + ':index:' + str(
                        getattr(request, 'trace_links_index')) + ':log info write error!!!')

    async def _init_trace_start_log_record(self, request: Request):
        """
        请求记录初始化
        :return:
        """

        path_info = request.url.path
        if path_info not in ['/favicon.ico'] and 'websocket' not in path_info:
            if request.method != 'OPTIONS':
                request.trace_links_index = 0
                request.traceid = str(uuid.uuid4()).replace('-', '')
                request.start_time = perf_counter()
                ip, method, url = request.client.host, request.method, request.url.path
                try:
                    body_form = await request.form()
                except :
                    body_form = None

                body = None
                try:
                    body_bytes = await request.body()
                    if body_bytes:
                        try:
                            body = await request.json()
                        except (TypeError, ValueError):
                            pass
                            if body_bytes:
                                try:
                                    body = body_bytes.decode('utf-8')
                                except JSONDecodeError:
                                    body = body_bytes.decode('gb2312')
                except Exception:
                    body = None
                    pass
                log_msg = {
                    'headers': request.headers if str(request.headers) else '',
                    'url': url,
                    'method': method,
                    'ip': ip,
                    'params': {
                        'query_params': '' if not request.query_params else request.query_params,
                        'from': str(body_form),
                        'body': body
                    },
                }
                await self.async_trace_add_log_record(request, event_des='request_start', msg_dict=log_msg)

    async def _init_trace_end_log_record(self, request: Request, response: Response):
        if hasattr(request, 'traceid'):
            start_time = getattr(request, 'start_time')
            end_time = f'{(perf_counter() - start_time):.2f}'
            resp_body = None
            if isinstance(response, Response):
                if response.headers.get('content-type') == 'application/json':
                    resp_body = json_to_dict(response.body)
                else:
                    try:
                        resp_body = str(response.body)
                    except AttributeError:
                        resp_body = ''
            log_msg = {
                'cost_time': end_time,
                'resp_body': resp_body
            }
            await self.async_trace_add_log_record(request, event_des='request_end', msg_dict=log_msg)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # 请求日志的初始化操作
            await self._init_trace_start_log_record(request)
            response: Response = await original_route_handler(request)
            # 日志收尾记录
            await self._init_trace_end_log_record(request, response)
            return response

        return custom_route_handler
