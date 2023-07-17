# -*- coding: utf-8 -*-
# @Time    : 2022/9/4 21:00
# @Author  : XJC
# @desc    :
from fastapi import APIRouter

from .routers import DkDnsRouter, DkDnsTypeRouter,DkTableRouter

router = APIRouter()
router.include_router(DkDnsTypeRouter().router)
router.include_router(DkDnsRouter().router)
router.include_router(DkTableRouter().router)
#
# # router.include_router(CRUDRouter(schema=DkDataSourceinfoSchema, db_model=DkDataSourceinfo, db=get_db, tags=["目录管理"]))

db_c_api = APIRouter()
db_c_api.include_router(router, prefix="/catalogs", )
