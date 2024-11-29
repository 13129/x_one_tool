from fastapi import APIRouter

from .dk_data_api import DkDnsRouter,DkTableRouter,DkCatalogRouter

dk_api = APIRouter()
dk_api.include_router(DkDnsRouter.instance(), prefix="/metaData")
dk_api.include_router(DkTableRouter.instance(), prefix="/metaData")
dk_api.include_router(DkCatalogRouter.instance(), prefix="/metaData")
