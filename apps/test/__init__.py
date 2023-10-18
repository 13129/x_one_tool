# -*- coding: utf-8 -*-
# @Time    : 2022/9/4 21:00
# @Author  : XJC
# @desc    :
from fastapi import APIRouter
from apps.test.models import DbTestRouter

router = APIRouter()
router.include_router(DbTestRouter.router)
db_test_api = APIRouter()
db_test_api.include_router(router, prefix="/test", )
