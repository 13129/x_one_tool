import os

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from setting import settings
from src import init_di
from src.common.middleware.router_class import ContextIncludedRoute
from xlogger import Loggers

os.environ["TZ"] = settings.TIMEZONE
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    log_level="info",
    docs_url=None,
    redoc_url=None,
    reload=settings.RELOAD,
    host=settings.HOST,
    port=settings.PORT
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_di(app)
app.mount('/static', StaticFiles(directory='static'), name='static')
app.router.route_class = ContextIncludedRoute


@app.get('/')
def root():
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
        redoc_js_url="static/swagger-ui/redoc.standalone.js",
    )


def custom_openapi():
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


app.openapi = custom_openapi

if __name__ == '__main__':
    # uvicorn.run(host='0.0.0.0',port=18899, app='main:app', reload=True, workers=1, log_level="debug")
    config = uvicorn.Config(app="main:app",
                            port=18899,
                            workers=1,
                            reload=True,
                            log_level='debug')
    server = uvicorn.Server(config=config)
    Loggers.init_config()

    server.run()
