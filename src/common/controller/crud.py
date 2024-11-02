from typing import Any, Callable, List, Type, Generator, Optional, Union

from src.base.crud_base import CRUDGenerator
from src.base.types import PYDANTIC_SCHEMA as SCHEMA

try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    from sqlalchemy.ext.declarative import DeclarativeMeta as Model, DeclarativeMeta
    from sqlalchemy.exc import IntegrityError
except ImportError:
    Model = None
    Session = None
    AsyncSession = None
    IntegrityError = None
    sqlalchemy_installed = False
else:
    sqlalchemy_installed = True
    Session = Callable[..., Generator[Session, Any, None]]

CALLABLE = Callable[..., Model]
CALLABLE_LIST = Callable[..., List[Model]]


class SQLAlchemyCRUDRouter(CRUDGenerator[SCHEMA]):
    def __init__(
            self,
            schema: Type[SCHEMA],
            db: Callable[..., Union["Session", "AsyncSession"]],
            prefix: Optional[str] = None,
            tags: Optional[List[str]] = None,
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
            tags: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        super().__init__(
            prefix=prefix,
            tags=tags,
            **kwargs
        )
