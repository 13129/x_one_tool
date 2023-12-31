from typing import Any, Callable, List, Type, Generator, Optional, Union

from fastapi import Depends, HTTPException
from apps.base import CRUDGenerator, NOT_FOUND
from apps.base import DEPENDENCIES, PAGINATION, PYDANTIC_SCHEMA as SCHEMA
from apps.base import get_pk_type

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
            db_model: Model,
            db: Callable[..., "AsyncSession"],
            create_schema: Optional[Type[SCHEMA]] = None,
            update_schema: Optional[Type[SCHEMA]] = None,
            delete_schema: Optional[Type[SCHEMA]] = None,
            prefix: Optional[str] = None,
            tags: Optional[List[str]] = None,
            paginate: Optional[int] = None,
            get_all_route: Union[bool, DEPENDENCIES] = True,
            get_one_route: Union[bool, DEPENDENCIES] = True,
            create_route: Union[bool, DEPENDENCIES] = True,
            update_route: Union[bool, DEPENDENCIES] = True,
            delete_one_route: Union[bool, DEPENDENCIES] = True,
            delete_all_route: Union[bool, DEPENDENCIES] = True,
            **kwargs: Any
    ) -> None:
        assert (
            sqlalchemy_installed
        ), "SQLAlchemy must be installed to use the SQLAlchemyCRUDRouter."

        self.db_model = db_model
        self.db_func = db
        self._pk: str = db_model.__table__.primary_key.columns.keys()[0]
        self._pk_col = db_model.__table__.c[self._pk]
        self._pk_type: type = get_pk_type(schema, self._pk)

        if db_model.__table__.columns.get('delete_status') is not None:
            self._del = 'delete_status'
        elif db_model.__table__.columns.get('DELETE_STATUS') is not None:
            self._del = 'DELETE_STATUS'
        else:
            self._del = None
            delete_one_route = False
            delete_all_route = False

        super().__init__(
            schema=schema,
            create_schema=create_schema,
            update_schema=update_schema,
            delete_schema=delete_schema,
            prefix=prefix or db_model.__tablename__,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs
        )

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
                db: Session = Depends(self.db_func),
                pagination: PAGINATION = self.pagination,
        ) -> List[Model]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            query = select(self.db_model).order_by(getattr(self.db_model, self._pk)).limit(limit).offset(skip)
            result = await db.execute(query)
            db_models: List[Model] = (result.scalars().all())
            return db_models

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
                item_id: self._pk_type, db: Session = Depends(self.db_func)  # type: ignore
        ) -> Model:
            query = select(self.db_model).where(self._pk_col == item_id)
            model: Model = await db.execute(query)

            if model:
                return model.scalar()
            else:
                raise NOT_FOUND from None

        return route

    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
                model: self.create_schema,  # type: ignore
                db: Session = Depends(self.db_func)
        ) -> Model:
            try:

                db_model: Model = self.db_model(**model.dict())
                db.add(db_model)
                await db.flush()
                # await db.commit()
                db.expunge(db_model)

                return db_model
                # db_model = insert(self.db_model).values(**model.dict())
                # last_record_id = await db.execute(db_model)
                # print({"id": last_record_id})
                # return None
            except IntegrityError:
                await db.rollback()
                raise HTTPException(422, "Key already exists") from None

        return route

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
                item_id: self._pk_type,  # type: ignore
                model: self.update_schema,  # type: ignore
                db: Session = Depends(self.db_func),
        ) -> Model:
            try:
                db_model: Model = await self._get_one()(item_id, db)

                for key, value in model.dict(exclude={self._pk}).items():
                    if hasattr(db_model, key):
                        setattr(db_model, key, value)

                await db.flush()
                db.expunge(db_model)

                return db_model
            except IntegrityError as e:
                await db.rollback()
                self._raise(e)

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(model: self.delete_schema, db: Session = Depends(self.db_func)) -> List[Model]:  # type: ignore
            if self._del:
                try:
                    for item in model.data:

                        db_model: Model = await self._get_one()(item.id, db)
                        for key, value in item.dict(exclude={self._pk}).items():
                            if hasattr(db_model, key):
                                setattr(db_model, key, value)
                    await db.flush()
                    db.expunge(db_model)
                    return db_model
                except IntegrityError as e:
                    await db.rollback()
                    self._raise(e)
            else:
                return None

            return self._get_all()(db=db, pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        def route(
                item_id: self._pk_type, db: Session = Depends(self.db_func)  # type: ignore
        ) -> Model:
            db_model: Model = self._get_one()(item_id, db)
            db.delete(db_model)
            db.commit()

            return db_model

        return route
