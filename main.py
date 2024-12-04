import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from setting import settings
from src import custom_static_openapi, init_di, lifespan
from src.common.middleware.router_class import ContextIncludedRoute

os.environ["TZ"] = settings.TIMEZONE
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    timezone=settings.TIMEZONE,
    log_level="info",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
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
app.openapi = custom_static_openapi(app)


@app.get('/')
def root():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run(host='127.0.0.1', port=18899, app='main:app', reload=True, workers=1, log_level="debug")
    # config = uvicorn.Config(app="main:app",
    #                         port=18899,
    #                         workers=1,
    #                         reload=True,
    #                         log_level='debug')
    # server = uvicorn.Server(config=config)
    # server.run()
