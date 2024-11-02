"""
coding:utf-8
@Time:2022/8/4 23:24
@Author:XJC
@Description:
"""
from fastapi.exceptions import HTTPException


class NotFoundError(HTTPException):
    entity_name: str

    def __init__(self, status_code, detail, headers, entity_id):
        super().__init__(status_code, f"{self.entity_name} not found, id: {entity_id}", headers)
