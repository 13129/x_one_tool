from fastapi import APIRouter

from .dk_data_api import (DkDnsRouter,
    # DkTableRouter,DkCatalogRouter
                          )

dk_api = APIRouter(prefix="/metaData")
dk_api.include_router(DkDnsRouter.instance())
# dk_api.include_router(DkTableRouter.instance())
# dk_api.include_router(DkCatalogRouter.instance())
