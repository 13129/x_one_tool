#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :xlog.py
@Time      :2024/12/4 16:52
@Author    :XJC
@Description:
"""
from src.common.utils.json_dp import dict_to_json_ensure_ascii
from src.core.container import BaseContainer
from fastapi import Request

class XLogMixin:
    logger = BaseContainer.logger().xlog

    @property
    def log(self):
        return self.logger

    async def async_trace_add_log_record(self,request: Request, event_des: str = None, msg_dict: dict = None,
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
                self.log.info(log_msg)
            except:
                self.log.info(
                    getattr(request, 'traceid') + ':index:' + str(
                        getattr(request, 'trace_links_index')) + ':log info write error!!!')
