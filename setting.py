"""
coding:utf-8
@Time:2022/8/4 22:40
@Author:XJC
@Description:
"""
import logging
import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseConfig
from pydantic import FilePath

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


class EnvironmentEnum(str, Enum):
    PRODUCTION = "production"
    LOCAL = "local"


class GlobalConfig(BaseConfig):
    TITLE: str = "DBTool"
    DESCRIPTION: str = "DB工具"

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "UTC"

    DATABASE_URL: Optional[FilePath] = os.path.join(BASE_DIR, "db.sqlite3")
    DB_ECHO_LOG: bool = False

    @property
    def async_database_url(self) -> Optional[str]:
        self.DATABASE_URL = "sqlite+aiosqlite:///{}/db.sqlite3".format(BASE_DIR)
        return self.DATABASE_URL if self.DATABASE_URL else self.DATABASE_URL

    # Api V1 prefix
    API_V1_STR = "/v1"

    class Config:
        case_sensitive = True


class LocalConfig(GlobalConfig):
    """Local configurations."""

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL


class ProdConfig(GlobalConfig):
    """Production configurations."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        if self.environment == EnvironmentEnum.LOCAL.value:
            return LocalConfig()
        return ProdConfig()


@lru_cache()
def get_configuration() -> GlobalConfig:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
