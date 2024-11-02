from fastapi import APIRouter

from .dk_data_source_api import DkDnsRouter
from .dk_table_api import DkTableRouter
from .dk_catalog_api import DkCatalogRouter

dk_api = APIRouter()
dk_api.include_router(DkDnsRouter.instance(), prefix="/metaData")
dk_api.include_router(DkTableRouter.instance(), prefix="/metaData")
dk_api.include_router(DkCatalogRouter.instance(), prefix="/metaData")
