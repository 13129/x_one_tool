#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :config.py.py
@Time      :2024/4/26 下午8:27
@Author    :XJC
@Description:
"""
import os
import sys
from pathlib import Path
from typing import List

from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminSite
from src.db.db_session import _engine

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BACKEND_DIR.__str__())


class Settings(admin.Settings):
    name: str = "FastAPI-User-Auth-Demo"
    secret_key: str = ""
    allow_origins: List[str] = []


# 设置FAA_GLOBALS环境变量
os.environ.setdefault("FAA_GLOBALS", "core.globals")

settings = Settings(_env_file=os.path.join(BACKEND_DIR, ".env"))
site = AdminSite(settings=settings, engine=_engine())
