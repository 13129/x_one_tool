# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :json_dp.py
@Time      :2024/1/5 18:39
@Author    :XJC
@Description:
"""
import datetime
import decimal
import json


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
            return dict(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# dict to json
def dict_to_json(dic: dict):
    return json.dumps(dic, cls=CJsonEncoder)


# json to dict
def json_to_dict(json_msg):
    dic = json.loads(s=json_msg)
    return dic


# 不格式化的输出ensure_ascii==false 输出中文的时候，保持中文的输出
def dict_to_json_ensure_ascii(dic: dict, ensure_ascii=False):
    return json.dumps(dic, cls=CJsonEncoder, ensure_ascii=ensure_ascii)


# 格式化排版缩进输出-ensure_ascii==false 输出中文的时候，保持中文的输出
def dict_to_json_ensure_ascii_indent(dic: dict, ensure_ascii=False):
    return json.dumps(dic, cls=CJsonEncoder, ensure_ascii=ensure_ascii, indent=4)
