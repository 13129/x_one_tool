# -*- coding: utf-8 -*-
# @Time    : 2022/9/4 21:00
# @Author  : XJC
# @desc    :
from fastapi import APIRouter
from apps.db_catlog.routers import DkDnsRouter, DkDnsTypeRouter, DkTableRouter, DkCatalogRouter, \
    DkCatalogTableRelationalRouter

router = APIRouter()
router.include_router(DkDnsTypeRouter.router)
router.include_router(DkDnsRouter.router)
router.include_router(DkTableRouter.router)
router.include_router(DkCatalogRouter.router)
router.include_router(DkCatalogTableRelationalRouter.router)

db_c_api = APIRouter()
db_c_api.include_router(router, prefix="/catalogs", )
