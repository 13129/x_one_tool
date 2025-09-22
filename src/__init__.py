#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName  :__init__.py.py
@Time      :2024/7/26 下午8:11
@Author    :XJC
@Description:
"""
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from setting import settings
from src.api import dk_api
from xlogger import Loggers
from src.module import Application


def init_di(app):
    container = Application()
    container.wire(modules=["src.api.v1.dk_data_api"])
    app.container = container
    app.include_router(dk_api, prefix=settings.API_V1_STR)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    Loggers.init_config()
    yield


def custom_static_openapi(app):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url='static/swagger-ui/swagger-ui-bundle.js',
            swagger_css_url='static/swagger-ui/swagger-ui.css',
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="static/swagger-ui/redoc.standalone.js",
        )

    def custom_openapi() -> Dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Custom title",
            version="2.5.0",
            openapi_version='3.0.2',
            summary="This is a very custom OpenAPI schema",
            description="Here's a longer description of the custom **OpenAPI** schema",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return custom_openapi
