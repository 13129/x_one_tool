from enum import Enum
from typing import Any, Callable, List, Optional, Type, Union

from src.core.crud_base import CRUDGenerator
from src.core.type import PYDANTIC_SCHEMA as SCHEMA

try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    from sqlalchemy.ext.declarative import DeclarativeMeta as Model, DeclarativeMeta
    from sqlalchemy.exc import IntegrityError
except ImportError:
    Session: Any  # no-redef
    AsyncSession: Any  # no-redef
    sqlalchemy_installed = False
else:
    sqlalchemy_installed = True


class SQLAlchemyCRUDRouter(CRUDGenerator[SCHEMA]):
    def __init__(
            self,
            schema: Type[SCHEMA],
            db: Callable[..., Union[Session, AsyncSession]],
            prefix: Optional[str] = None,
            tags: Optional[List[Union[str, Enum]]] = None,
            **kwargs: Any
    ) -> None:
        assert (
            sqlalchemy_installed
        ), "SQLAlchemy must be installed to use the SQLAlchemyCRUDRouter."

        self.db_func = db

        super().__init__(
            schema=schema,
            prefix=prefix,
            tags=tags,
            **kwargs
        )


class VCRUDRouterBase(CRUDGenerator[SCHEMA]):
    def __init__(
            self,
            prefix: Optional[str] = None,
            tags: Optional[List[Union[str, Enum]]] = None,
            **kwargs: Any
    ) -> None:
        super().__init__(
            prefix=prefix,
            tags=tags,
            **kwargs
        )
