from pydantic import BaseModel


class BaseModelSchema(BaseModel):
    id: str

    class Config:
        orm = False
