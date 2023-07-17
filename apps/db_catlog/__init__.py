# -*- coding: utf-8 -*-
# @Time    : 2022/9/4 21:00
# @Author  : XJC
# @desc    :
from fastapi import APIRouter
from apps.db_catlog.routers import (dk_dns_router, dk_table_router, dk_catalog_router, dk_dns_type_router,
                                    dk_catalog_table_relation)

router = APIRouter()
router.include_router(dk_dns_type_router)
router.include_router(dk_dns_router)
router.include_router(dk_table_router)
router.include_router(dk_catalog_router)
router.include_router(dk_catalog_table_relation)

db_c_api = APIRouter()
db_c_api.include_router(router, prefix="/catalogs", )
