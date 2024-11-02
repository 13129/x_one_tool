from fastapi import APIRouter

from .dk_data_source import DkDnsRouter
from .dk_table import DkTableRouter

dk_api = APIRouter()
dk_api.include_router(DkDnsRouter.instance(), prefix="/metaData")
dk_api.include_router(DkTableRouter.instance(), prefix="/metaData")
