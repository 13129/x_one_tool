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
    def sync_trace_add_log_record(request: Request, event_des='', msg_dict=None, remarks=''):
        """

        :param request:
        :param event_des: 日志记录事件描述
        :param msg_dict: 日志记录信息字典
        :param remarks: 日志备注信息
        :return:
        """
        # request.request_links_index = request.request_links_index + 1
        if msg_dict is None:
            msg_dict = {}
        if hasattr(request, 'traceid'):
            loggers.info(request)
            log = {
                # 自定义一个新的参数复制到我们的请求上下文的对象中
                'traceid': getattr(request, 'traceid'),
                # 定义链路所以序号
                'trace_index': getattr(request, 'trace_links_index'),
                # 日志时间描述
                'event_des': event_des,
                # 日志内容详情
                'msg_dict': msg_dict,
                # 日志备注信息
                'remarks': remarks
            }
            #  为少少相关记录，删除不必要的为空的日志内容信息，
            if not remarks:
                log.pop('remarks')
            if not msg_dict:
                log.pop('msg_dict')
            try:
                log_msg = dict_to_json_ensure_ascii(log)  # 返回文本
                loggers.info(log_msg)
            except:
                loggers.info(
                    getattr(request, 'traceid') + '：索引：' + str(getattr(request, 'trace_links_index')) + ':日志信息写入异常')

    # 封装一下关于记录序号的日志记录用于全链路的日志请求的日志
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

        # request.request_links_index = request.request_links_index + 1
        # 如果没有这个标记的属性的，说明这个接口的不需要记录啦！
        if hasattr(request, 'traceid'):
            log = {
                # 自定义一个新的参数复制到我们的请求上下文的对象中
                'traceid': getattr(request, 'traceid'),
                # 定义链路所以序号
                'trace_index': getattr(request, 'trace_links_index'),
                # 日志时间描述
                'event_des': event_des,
                # 日志内容详情
                'msg_dict': msg_dict,
                # 日志备注信息
                'remarks': remarks
            }
            #  为少少相关记录，删除不必要的为空的日志内容信息，
            if not remarks:
                log.pop('remarks')
            if not msg_dict:
                log.pop('msg_dict')
            try:
                log_msg = dict_to_json_ensure_ascii(log)  # 返回文本
                loggers.info(log_msg)
            except:
                loggers.info(
                    getattr(request, 'traceid') + '：索引：' + str(getattr(request, 'trace_links_index')) + ':日志信息写入异常')

    async def _init_trace_start_log_record(self, request: Request):
        """
        请求记录初始化
        :return:
        """

        path_info = request.url.path
        if path_info not in ['/favicon.ico'] and 'websocket' not in path_info:
            if request.method != 'OPTIONS':
                # 追踪索引
                request.trace_links_index = 0
                # 追踪ID
                request.traceid = str(uuid.uuid4()).replace('-', '')
                # 计算时间
                request.start_time = perf_counter()
                # 获取请求来源的IP,请求的方法
                ip, method, url = request.client.host, request.method, request.url.path
                # 先看表单有没有数据：
                try:
                    body_form = await request.form()
                except:
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
                    # 记录请求头信息
                    'headers': request.headers if str(request.headers) else '',
                    # 记录请求URL信息
                    'url': url,
                    # 记录请求方法
                    'method': method,
                    # 记录请求来源IP
                    'ip': ip,
                    'params': {
                        'query_params': '' if not request.query_params else request.query_params,
                        'from': str(body_form),
                        'body': body
                    },
                }
                # 执行写入--日志具体的内容信息
                await self.async_trace_add_log_record(request, event_des='请求开始', msg_dict=log_msg)

    async def _init_trace_end_log_record(self, request: Request, response: Response):
        if hasattr(request, 'traceid'):
            start_time = getattr(request, 'start_time')
            end_time = f'{(perf_counter() - start_time):.2f}'
            # 获取响应报文信息内容
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
                # 记录请求耗时
                'cost_time': end_time,
                #  记录请求响应的最终报文信息
                'resp_body': resp_body
            }
            await self.async_trace_add_log_record(request, event_des='请求结束', msg_dict=log_msg)

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
