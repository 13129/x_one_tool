import os

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from setting import settings
from apps.db_catlog import db_c_api as db_c_api

os.environ["TZ"] = settings.TIMEZONE
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    # log_level="info",
    docs_url=None,
    redoc_url=None,
    # openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(db_c_api, prefix=settings.API_V1_STR)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.on_event("startup")
async def startup_event():
    print("-----启动应用程序啦-----")
    print("-----启动数据库可用性检查-----")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
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
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True,workers=3)
