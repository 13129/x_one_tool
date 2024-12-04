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
from typing import Callable, Optional

from fastapi import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute

from xlogger import log as loggers
from .json_dp import dict_to_json_ensure_ascii, json_to_dict


class ContextIncludedRoute(APIRoute):

    @staticmethod
    async def async_trace_add_log_record(request: Request,
                                         event_des: Optional[str] = None,
                                         msg_dict: Optional[dict] = None,
                                         remarks: Optional[str] = None):
        """
        :param request:
        :param event_des: 日志记录事件描述
        :param msg_dict: 日志记录信息字典
        :param remarks: 日志备注信息
        :return:
        """

        if hasattr(request, 'traceid'):
            _log = {
                'traceid': getattr(request, 'traceid'),
                'trace_index': getattr(request, 'trace_links_index'),
                'event_des': event_des,
                'msg_dict': msg_dict,
                'remarks': remarks
            }
            if not remarks:
                _log.pop('remarks')
            if not msg_dict:
                _log.pop('msg_dict')
            try:
                _msg = dict_to_json_ensure_ascii(_log)
                loggers.info(_msg)
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
                request.state.trace_links_index = 0
                request.state.traceid = str(uuid.uuid4()).replace('-', '')
                request.state.start_time = perf_counter()
                ip = None
                method = None
                url = None
                if request.client is not None:
                    ip, method, url = request.client.host, request.method, request.url.path
                try:
                    _form = await request.form()
                except:
                    _form = None

                _body = None
                try:
                    _bytes = await request.body()
                    if _bytes:
                        try:
                            _body = await request.json()
                        except (TypeError, ValueError):
                            pass
                            if _bytes:
                                try:
                                    _body = _bytes.decode('utf-8')
                                except JSONDecodeError:
                                    _body = _bytes.decode('gb2312')
                except Exception:
                    _body = None
                finally:
                    _msg = {
                        'headers': request.headers if str(request.headers) else '',
                        'url': url,
                        'method': method,
                        'ip': ip,
                        'params': {
                            'query_params': '' if not request.query_params else request.query_params,
                            'from': str(_form),
                            'body': _body
                        },
                    }
                    await self.async_trace_add_log_record(request, event_des='request_start', msg_dict=_msg)

    async def _init_trace_end_log_record(self, request: Request, response: Response):
        if hasattr(request, 'traceid'):
            start_time = getattr(request, 'start_time')
            end_time = f'{(perf_counter() - start_time):.2f}'
            _body = None
            if isinstance(response, Response):
                if response.headers.get('content-type') == 'application/json':
                    _body = json_to_dict(response.body)
                else:
                    try:
                        _body = str(response.body)
                    except AttributeError:
                        _body = ''
            _msg = {
                'cost_time': end_time,
                'resp_body': _body
            }
            await self.async_trace_add_log_record(request, event_des='request_end', msg_dict=_msg)

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
