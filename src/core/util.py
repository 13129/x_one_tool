from fastapi import HTTPException


class AttrDict(dict):  # type: ignore
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg, "type": "type_error.integer"}
            ]
        },
    )

