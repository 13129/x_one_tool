from typing import Optional, Type, Any, List, Dict

from fastapi import Depends, HTTPException
from pydantic import create_model

from ._types import T, PAGINATION, PYDANTIC_SCHEMA


class AttrDict(dict):  # type: ignore
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_pk_type(schema: Type[PYDANTIC_SCHEMA], pk_field: str) -> Any:
    try:
        # print("效验", (schema.model_fields[pk_field]))
        return schema.model_fields[pk_field].annotation
    except KeyError:
        return int


def schema_factory(
        schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """
    Is used to create a CreateSchema which does not contain pk
    """
    fields = {
        f: (schema_cls.model_fields[f].annotation, ...)
        for f in schema_cls.model_fields
        if f != pk_field_name
    }
    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
    return schema


def delete_schema_factory(
        schema_cls: Type[T], pk_field_name: str = "id", del_field_name: str = 'delete_status', name: str = "Delete",
) -> Type[T]:
    """
    Is used to create a CreateSchema  pk
    """
    fields = {
        f: (schema_cls.model_fields[f].annotation, ...)
        for f in schema_cls.model_fields
        if f == pk_field_name or f == del_field_name
    }
    data = {"data": (List[create_model(__model_name=__name__ + name, **fields)], ...)}
    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(__model_name=name, **data)  # type: ignore
    return schema


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg, "type": "type_error.integer"}
            ]
        },
    )


def pagination_factory(max_limit: Optional[int] = None) -> Any:
    """
    Created the pagination dependency to be used in the router
    """

    def pagination(skip: int = 0, limit: Optional[int] = max_limit) -> PAGINATION:
        if skip < 0:
            raise create_query_validation_exception(
                field="skip",
                msg="skip query parameter must be greater or equal to zero",
            )

        if limit is not None:
            if limit <= 0:
                raise create_query_validation_exception(
                    field="limit", msg="limit query parameter must be greater then zero"
                )

            elif max_limit and max_limit < limit:
                raise create_query_validation_exception(
                    field="limit",
                    msg=f"limit query parameter must be less then {max_limit}",
                )

        return {"skip": skip, "limit": limit}

    return Depends(pagination)
